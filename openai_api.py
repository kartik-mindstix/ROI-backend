import openai
import pandas as pd
import json

# Function to load and preprocess CSV data using pandas
def load_csv_data(csv_file_path):
    try:
        data = pd.read_csv(csv_file_path)
        return data
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

# Function to create a detailed marketing analyst prompt based on CSV columns
def create_marketing_prompt(data):
    columns = data.columns.tolist()
    return f"""
    You are an expert marketing analyst. Analyze the following dataset and provide insights:

    Columns:
    medium: A categorical column indicating the type of marketing medium (e.g., "Direct", "Search", "Referral", etc.). It would be useful for analyzing conversion rates across different mediums.
    conversion: Integer values representing the number of conversions. Useful for tracking how many successful actions (conversions) were achieved via each medium.
    fullVisitorId: Integer identifier for visitors. It could indicate unique visitors or sessions, relevant for understanding user behavior and journey analysis.
    conversion_rate: Text values with percentages (e.g., "3.3%", "1.3%"). It represents the percentage of visitors who converted. This column would need to be converted into numerical format for proper analysis.
    converted_user_journey: This column contains lists where each element represents:
    The user journey, which is a sequence of mediums the user interacted with before converting.
    The number of conversions associated with that specific journey.
    non_converted_user_journey: This column contains lists structured similarly to the converted journey column, but it tracks journeys where users did not convert. Each element represents:
    The user journey, which shows the sequence of mediums the user interacted with.
    he number of non-conversions (i.e., instances where users followed this path but did not convert).
    to_state: Represents the edges showing where the user journey leads after interacting with the current medium. Similarly, each list element contains:
    The state to which the user moves (e.g., "(conversion)" or another channel).
    The probability of moving from the current state to the next.
    from_state: Represents the edges that show where the user journey begins (i.e., the "from" states). Each list element contains two components:
    The state from which the user came (e.g., "(start)" or another channel).
    The probability of transitioning from that state to the current medium.
    channel_name_x: Categorical column representing the name of the channel that brought users (e.g., "Direct", "Search"). This is useful for channel attribution analysis.
    total_conversions: Floating-point values, representing the total number of conversions attributed to a channel or medium. Important for determining the effectiveness of each marketing strategy.
    total_conversion_value: Floating-point values indicating the total monetary value of conversions from each medium. This column would be used to measure the revenue impact of conversions.
    channel_name_y: Another categorical column representing the channel name. Its presence, along with channel_name_x, raises the question of whether there’s a distinction between the two, or if they represent the same data.
    removal_effects_conversion: Floating-point values representing the percentage effect of removing a channel from the conversion path. This is useful for analyzing channel importance in multi-touch attribution.
    removal_effects_conversion_value: Floating-point values showing the monetary effect of removing a channel. This helps in understanding how important each channel is in terms of revenue.

    Please analyze the best and worst user journeys based on conversion rates and value, and provide the ideal budget allocation for the channels to maximize conversions.

    Suggest a detailed explanation and actionable steps to improve the performance.
    """

# Function to interact with the OpenAI API and query ChatGPT
def query_chatgpt(api_key, prompt, model="gpt-4"):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a marketing analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error querying ChatGPT: {e}")
        return None

# Function to get insights from ChatGPT based on CSV data and return strict JSON format
def get_marketing_insights(api_key, csv_file_path, user_history):
    # Load the CSV data using pandas
    data = load_csv_data(csv_file_path)
    if data is None:
        return None
    
    # Create a prompt for ChatGPT based on the loaded data
    prompt = create_marketing_prompt(data)

    # Query ChatGPT with the detailed marketing prompt
    insights = query_chatgpt(api_key, prompt)
    
    if insights:
        # Keep user history (append the insights)
        user_history.append({
            "prompt": prompt,
            "response": insights
        })

        # Return insights in strict JSON format for frontend consumption
        response = {
            "best_user_journey": "To be determined by GPT",  # placeholder for GPT response
            "worst_user_journey": "To be determined by GPT",  # placeholder for GPT response
            "budget_allocation": "To be determined by GPT",   # placeholder for GPT response
            "insights": insights
        }
        return response
    else:
        return None

# Function to generate insights and save to JSON while maintaining user history
def generate_insights_json(api_key, csv_file_path, output_json_path, user_history):
    insights_json = get_marketing_insights(api_key, csv_file_path, user_history)
    if insights_json:
        try:
            with open(output_json_path, 'w') as json_file:
                json.dump(insights_json, json_file, indent=4)
            print(f"Insights generated and saved to {output_json_path}")
        except Exception as e:
            print(f"Error writing to JSON file: {e}")
    else:
        print("No insights generated.")

# Initialize user history as a list
user_history = []

