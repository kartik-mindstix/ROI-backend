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
    - conversion_rate: The rate of conversions from users visiting a platform to taking a desired action (e.g., making a purchase, signing up).
    - converted_user_journeys: User journeys that resulted in conversions across different marketing channels.
    - frequency: The number of times users interacted with specific marketing channels before converting.
    - budget_allocation: The percentage of the total marketing budget allocated to each channel.

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

