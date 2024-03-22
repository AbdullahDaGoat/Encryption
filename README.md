**Index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Healthcard App</title>

    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
            font-family: 'Helvetica', Arial, sans-serif;
        }

        .container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 6px;
            text-align: center;
        }

        h1 {
            margin-bottom: 30px;
            color: #007bff;
        }

        form {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1em;
        }

        label {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #555;
        }

        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
        }

        button {
            background-color: #007bff;
            color: #fff;
            padding: 10px;
            border: none;
            width: 400px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }

        #response {
            margin-top: 20px;
            padding: 20px;
            background-color: #f3f3f3;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #333;
            text-align: left;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Healthcard App</h1>
        <form id="healthcard-form">
            <label for="healthcard">Healthcard Number:</label>
            <input type="text" id="healthcard" name="healthcard" required />
            <button type="submit">Submit</button>
        </form>
        <div id="response"></div>
    </div>

    <script>
        const form = document.getElementById('healthcard-form');
        const responseDiv = document.getElementById('response');

        form.addEventListener('submit', (event) => {
            event.preventDefault();
            const healthcard = document.getElementById('healthcard').value;

            fetch('http://localhost:5000/save-healthcard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ healthcard })
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Error: ' + response.status);
                }
            })
            .then(data => {
                localStorage.setItem('healthcard', healthcard);
                localStorage.setItem('response', JSON.stringify(data.savedText));
                responseDiv.textContent = `Response: ${data.savedText}`;
                responseDiv.style.display = 'block';
            })
            .catch(error => {
                responseDiv.textContent = `Error: ${error}`;
                responseDiv.style.display = 'block';
            });
        });

        const healthcard = localStorage.getItem('healthcard');
        const storedResponse = localStorage.getItem('response');

        if (healthcard && storedResponse) {
            console.log('Healthcard:', healthcard);
            console.log('Response:', JSON.parse(storedResponse));
        }
    </script>
</body>
</html>
```

**app.py:**
```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/save-healthcard', methods=['POST', 'GET'])
def save_healthcard():
    if request.method == 'POST':
        try:
            data_healthcard = request.get_json()
            healthcard = data_healthcard.get('healthcard')
            
            if healthcard is None:
                return jsonify({'error': 'Missing healthcard number'}), 400
            
            return jsonify({'savedText': 'Jacob'}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif request.method == 'GET':
        try:
            healthcard = request.args.get('healthcard')
            
            if healthcard is None:
                return jsonify({'error': 'Missing healthcard number'}), 400
            
            return jsonify({'savedText': 'Jacob'}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
     else:
	   return "Invalid Request" 

if __name__ == '__main__':
    app.run()
```
