<h1>Swipe right on Bumble</h1> <br>
This app will swipe right for user until reach end of likes for day:
<h1>Requirments:</h1> <br>
<p>This app utilizes Python3, Selenium, and Chrome.</p><br>
<p>Python3 can be found here: https://www.python.org/downloads/ </p><br>
<p>Selenium can be found here: http://www.seleniumhq.org/download/ </p><br>

<p> pip install --upgrade pip</p>
<p>pip install -r requirements.txt</p>

5. Configure Chrome WebDriver:
   - Open `parameters/bumble.py`
   - Set your Chrome WebDriver path:
   ```python
   self.driver = webdriver.Chrome("path/to/your/chromedriver")
   ```

## How to Use

1. Run the application:
```bash
python3 swipe_right.py
```

2. Open your browser and go to:
```
http://127.0.0.1:5000
```

3. Log in to Bumble using:
   - Facebook account, or
   - Phone number

## Troubleshooting

If you see "Driver not found" error:
- Check if Chrome WebDriver is installed
- Make sure Chrome WebDriver version matches your Chrome browser version
- Verify the path in `parameters/bumble.py` is correct
