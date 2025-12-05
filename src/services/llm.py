"""
Enhanced LLM service with context-aware prompts for Ollama
"""

import subprocess
import json
from typing import Dict, Optional
from datetime import datetime


class OllamaService:
    """
    Service for interacting with Ollama LLM with rich context
    """

    def __init__(self, model: str = "llama3:8b"):
        self.model = model

    def generate_response(self, prompt: str, max_retries: int = 2, timeout: int = 180) -> str:
        """
        Generate a response from Ollama
        """
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"

        except subprocess.TimeoutExpired:
            return "Error: Request timed out. Please try again."
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def create_personalized_analysis_prompt(
        self,
        user_data: Dict,
        climate_context: Dict,
        historical_stats: Optional[Dict] = None,
        location: Optional[str] = None,
        user_guidance: Optional[str] = None
    ) -> str:
        """
        Create a rich, personalized prompt for carbon footprint analysis
        """
        total = user_data['total_emissions']
        breakdown = user_data.get('breakdown', {})

        prompt = f"""You are an expert climate scientist and sustainability advisor. Analyze this person's carbon footprint with deep insight and actionable recommendations.

## CURRENT CONTEXT
- Date: {datetime.now().strftime('%B %d, %Y')}
- Atmospheric CO₂: {climate_context.get('atmospheric_co2_ppm', 425):.1f} ppm (Source: {climate_context.get('co2_source', 'NOAA')})
- Paris Agreement Target: Stay below 1.5°C warming → requires {climate_context.get('daily_co2_budget_kg', 6.0)} kg CO₂/day per person
- Latest Climate News: {climate_context.get('climate_headline', 'Climate action remains urgent')}
"""

        if climate_context.get('grid_intensity'):
            intensity = climate_context['grid_intensity']
            prompt += f"- Current Grid Carbon Intensity: {intensity.get('actual', 'N/A')} gCO₂/kWh ({intensity.get('index', 'moderate')} - {intensity.get('source', 'UK')})\n"

        if location:
            prompt += f"- User Location: {location}\n"

        if user_guidance:
            prompt += f"\n## USER'S SPECIFIC GUIDANCE\n{user_guidance}\n"

        prompt += f"""
## USER'S DAILY FOOTPRINT
- **Total Daily Emissions: {total:.2f} kg CO₂**
- Transport: {breakdown.get('Transport', 0):.2f} kg CO₂ ({user_data.get('transport_mode', 'unknown')}, {user_data.get('distance_km', 0)} km)
- Diet: {breakdown.get('Diet', 0):.2f} kg CO₂ ({user_data.get('diet_type', 'unknown')})
- Heating: {breakdown.get('Heating', 0):.2f} kg CO₂ ({user_data.get('heating_type', 'unknown')}, {user_data.get('heating_hours', 0)} hours)
- Electricity: {breakdown.get('Electricity', 0):.2f} kg CO₂ ({user_data.get('electricity_kwh', 0)} kWh)
- Consumption: {breakdown.get('Consumption', 0):.2f} kg CO₂
"""

        if historical_stats and historical_stats.get('record_count', 0) > 0:
            prompt += f"""
## HISTORICAL TREND ({historical_stats.get('period_days', 30)} days)
- Average Daily: {historical_stats.get('avg_daily_emissions', 0):.2f} kg CO₂
- Best Day: {historical_stats.get('min_emissions', 0):.2f} kg CO₂
- Worst Day: {historical_stats.get('max_emissions', 0):.2f} kg CO₂
- Total Emissions: {historical_stats.get('total_emissions', 0):.1f} kg CO₂
- Trend: {'Improving' if total < historical_stats.get('avg_daily_emissions', total) else 'Needs attention'}
"""

        prompt += f"""
## YOUR TASK
Provide a comprehensive, personalized sustainability analysis:

1. **Impact Assessment** (2-3 sentences)
   - Where does this person stand vs the Paris Agreement target ({climate_context.get('daily_co2_budget_kg', 6.0)} kg/day)?
   - What's the biggest contributor to their footprint?
   - If they maintain this rate, what's their annual impact?

2. **Top 3 Personalized Recommendations**
   For each recommendation:
   - Be SPECIFIC to their actual usage (don't suggest generic advice)
   - Quantify potential CO₂ savings
   - Explain how it helps the climate
   - Make it actionable (what exactly should they do?)"""

        if user_guidance:
            prompt += f"""
   - IMPORTANT: Pay special attention to the user's specific guidance and tailor your recommendations accordingly"""

        prompt += """


3. **Positive Recognition**
   - Highlight what they're doing well
   - Show how their actions contribute to climate goals

4. **Long-term Perspective**
   - Connect their daily choices to global climate impact
   - Inspire hope and agency

Keep the tone encouraging, scientific, and action-oriented. Use data and numbers to make it concrete.
"""

        return prompt

    def create_comparative_analysis_prompt(
        self,
        current_total: float,
        previous_total: float,
        categories: Dict
    ) -> str:
        """
        Create a prompt for comparing current vs previous footprint
        """
        change = current_total - previous_total
        change_pct = (change / previous_total * 100) if previous_total > 0 else 0

        prompt = f"""You are a sustainability coach analyzing carbon footprint changes.

## CHANGE ANALYSIS
- Previous: {previous_total:.2f} kg CO₂/day
- Current: {current_total:.2f} kg CO₂/day
- Change: {change:+.2f} kg CO₂/day ({change_pct:+.1f}%)

## CATEGORY BREAKDOWN
{json.dumps(categories, indent=2)}

## YOUR TASK
1. Analyze what drove the change (which categories changed most?)
2. If improved: Celebrate the progress and encourage consistency
3. If worse: Identify causes without judgment, suggest corrections
4. Provide 2 specific next steps

Keep it brief (4-5 sentences), encouraging, and actionable.
"""
        return prompt

    def create_goal_setting_prompt(
        self,
        current_avg: float,
        target: float = 6.0
    ) -> str:
        """
        Create a prompt for setting realistic carbon reduction goals
        """
        reduction_needed = current_avg - target
        reduction_pct = (reduction_needed / current_avg * 100) if current_avg > 0 else 0

        prompt = f"""You are a climate action strategist helping someone set carbon reduction goals.

## CURRENT SITUATION
- Current Average: {current_avg:.2f} kg CO₂/day
- Paris Agreement Target: {target} kg CO₂/day
- Reduction Needed: {reduction_needed:.2f} kg CO₂/day ({reduction_pct:.1f}% reduction)

## YOUR TASK
Design a realistic 3-month action plan:

1. **Month 1 Goal**: What's an achievable first step? (aim for 10-20% reduction)
2. **Month 2 Goal**: Build on month 1 progress
3. **Month 3 Goal**: Reach a sustainable level closer to the target

For each month:
- Set a specific emissions target
- Suggest 1-2 concrete actions
- Explain the expected impact

Keep it motivating and achievable. Break down big goals into manageable steps.
"""
        return prompt

    def analyze_footprint(
        self,
        user_data: Dict,
        climate_context: Dict,
        historical_stats: Optional[Dict] = None,
        location: Optional[str] = None,
        user_guidance: Optional[str] = None
    ) -> str:
        """
        Main method to analyze carbon footprint
        """
        prompt = self.create_personalized_analysis_prompt(
            user_data, climate_context, historical_stats, location, user_guidance
        )
        return self.generate_response(prompt)

    def compare_footprints(
        self,
        current_total: float,
        previous_total: float,
        categories: Dict
    ) -> str:
        """
        Compare current vs previous footprint
        """
        prompt = self.create_comparative_analysis_prompt(
            current_total, previous_total, categories
        )
        return self.generate_response(prompt)

    def create_action_plan(self, current_avg: float, target: float = 6.0) -> str:
        """
        Create a carbon reduction action plan
        """
        prompt = self.create_goal_setting_prompt(current_avg, target)
        return self.generate_response(prompt)


if __name__ == "__main__":
    # Test the service
    service = OllamaService()

    test_data = {
        'total_emissions': 15.5,
        'breakdown': {
            'Transport': 5.0,
            'Diet': 5.0,
            'Heating': 3.0,
            'Electricity': 2.5
        },
        'transport_mode': 'car_petrol',
        'distance_km': 25,
        'diet_type': 'omnivore',
        'heating_type': 'natural_gas',
        'heating_hours': 4,
        'electricity_kwh': 10
    }

    climate_context = {
        'atmospheric_co2_ppm': 425.0,
        'co2_source': 'NOAA',
        'daily_co2_budget_kg': 6.0,
        'climate_headline': 'Arctic ice continues to decline'
    }

    print("Testing LLM Service...")
    print("\nPrompt Preview:")
    prompt = service.create_personalized_analysis_prompt(test_data, climate_context)
    print(prompt[:500] + "...")
