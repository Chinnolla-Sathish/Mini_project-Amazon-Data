from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for rendering plots

app = Flask(__name__)

# Ensure the 'static' directory exists to save the plot
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/second')
def second_page():
    return render_template('second.html')

@app.route('/third')
def third_page():
    return render_template('third.html')

@app.route('/upload', methods=['POST'])
def upload():
    csv_file = request.files['csv_file']

    # Check if the file is a CSV
    if not csv_file.filename.endswith('.csv'):
        return "Error: Only CSV files are allowed."

    try:
        # Read the CSV file
        csv_data = pd.read_csv(csv_file)

        # Debug: Print column names
        print(csv_data.columns)

        # Strip spaces from column names
        csv_data.columns = csv_data.columns.str.strip()

        # Check if the necessary columns exist
        if 'Total Charged' not in csv_data.columns or 'Order Date' not in csv_data.columns:
            return "Error: Required columns 'Total Charged' and 'Order Date' not found in the CSV file."

        # Normalize the date format
        csv_data['Order Date'] = pd.to_datetime(csv_data['Order Date'], errors='coerce')

        # Remove rows with invalid dates
        csv_data = csv_data.dropna(subset=['Order Date'])

        # Calculate the total charged
        total_charged = csv_data["Total Charged"].fillna(0).sum()

        # Plotting the data
        plt.figure(figsize=(6, 5.9))
        plt.bar(csv_data['Order Date'].dt.strftime('%Y-%m-%d'), csv_data['Total Charged'])
        plt.xlabel('Order Date')
        plt.xticks(rotation=90)
        plt.ylabel('Total Charged (Rs.)')
        plt.title('Spendings Over Time')

        # Save the plot to the static directory
        plt.savefig('static/graph.png', dpi=200)
        plt.close()  # Close the plot to free up memory

        return render_template('fourth.html', csv_data=csv_data, total_charged=total_charged)

    except Exception as e:
        return f"Error processing file: {e}"

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for
# import pandas as pd
# import matplotlib.pyplot as plt
#
# app = Flask(__name__)
#


# @app.route('/')
# def home():
#     return render_template('home.html')
#
# @app.route('/second')
# def second_page():
#     return render_template('second.html')
#
#
# @app.route('/third')
# def third_page():
#     return render_template('third.html')
#
# @app.route('/upload', methods=['POST'])
# def upload():
#     csv_file = request.files['csv_file']
#     csv_data = pd.read_csv(csv_file)
#
#     #csv_data["Order Date"] = csv_data["Order Date"].str.replace('Z','').astype(float)
#     total_charged=csv_data["Total Owed"].sum()
#     plt.figure(figsize=(6, 5.9))
#     plt.bar(csv_data['Order Date'], csv_data['Total Owed'])
#     plt.xlabel('Order')
#     plt.xticks(rotation=90)
#     plt.ylabel('Rs.')
#     plt.title('Spendings/Dates')
#
#     plt.savefig('static/graph.png',dpi=200)
#
#     return render_template('fourth.html',csv_data=csv_data,total_charged=total_charged)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
