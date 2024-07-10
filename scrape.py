from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def scrape_books():
    # 初始化 Chrome 浏览器
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # 访问目标网页
    url = 'https://www.kobo.com/zh/blog/weekly-dd99-2024-w27'
    driver.get(url)

    # 等待页面加载完成
    driver.implicitly_wait(10)

    # 抓取所有 .book-block 元素
    book_blocks = driver.find_elements(By.CSS_SELECTOR, '.book-block')

    # 提取每个 book-block 的信息
    books = []
    for book_block in book_blocks:
        title = book_block.find_element(By.CSS_SELECTOR, '.title').text
        author = book_block.find_element(By.CSS_SELECTOR, '.author').text

        books.append({
            'title': title,
            'author': author
        })

    # 关闭浏览器
    driver.quit()

    return books

@app.route('/scrape', methods=['GET'])
def scrape_route():
    try:
        books = scrape_books()
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5505)

# 請求 http://localhost:5505/scrape
