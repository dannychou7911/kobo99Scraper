const express = require('express');
const { Builder, By } = require('selenium-webdriver');
require('chromedriver');

const app = express();

async function scrapeBooks() {
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // 访问目标网页
        const url = 'https://www.kobo.com/zh/blog/weekly-dd99-2024-w27';
        await driver.get(url);

        // 等待页面加载完成
        await driver.sleep(10000); // 等待10秒，以确保页面完全加载

        // 抓取所有 .book-block 元素
        let bookBlocks = await driver.findElements(By.css('.book-block'));

        // 提取每个 book-block 的信息
        let books = [];
        for (let bookBlock of bookBlocks) {
            let title = await bookBlock.findElement(By.css('.title')).getText();
            let author = await bookBlock.findElement(By.css('.author')).getText();

            books.push({
                title: title,
                author: author,
            });
        }

        return books;
    } finally {
        // 关闭浏览器
        await driver.quit();
    }
}

app.get('/scrape', async (req, res) => {
    try {
        const books = await scrapeBooks();
        res.json(books);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.listen(5505, () => {
    console.log('Server is running on http://localhost:5505');
});
