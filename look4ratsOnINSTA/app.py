from flask import Flask, render_template, request, flash, redirect, url_for
import csv
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database connection function
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hhkn3481$",
        database="follow"
    )

# Other functions from your original script (create_tables, insert_data, etc.)
# ... (copy them here)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'following_file' not in request.files or 'followers_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        following_file = request.files['following_file']
        followers_file = request.files['followers_file']
        
        if following_file.filename == '' or followers_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if following_file and followers_file:
            create_tables()
            
            # Save and process files
            following_file.save(following_file.filename)
            followers_file.save(followers_file.filename)
            
            process_csv_file(following_file.filename, "following", split_following)
            process_csv_file(followers_file.filename, "followers", split_followers)
            
            # Clean up files
            os.remove(following_file.filename)
            os.remove(followers_file.filename)
            
            return redirect(url_for('results'))
    
    return render_template('index.html')

@app.route('/results')
def results():
    non_followers = find_non_followers()
    drop_tables()
    return render_template('results.html', non_followers=non_followers)

if __name__ == '__main__':
    app.run(debug=True)