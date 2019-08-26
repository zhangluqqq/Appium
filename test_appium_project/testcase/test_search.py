from time import sleep
from appium import webdriver
import pytest
from selenium.webdriver.common.by import By


class TestAppium:
    def setup(self):
        caps = {
            "platformName": "android",
            "deviceName": "hogwarts",
            "appPackage": "com.xueqiu.android",
            "appActivity": ".view.WelcomeActivityAlias",
            "autoGrantPermissions": True
            }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(10)

    def teardown(self):
        sleep(5)
        self.driver.quit()

    def test_wrong_phone(self):
        self.driver.find_element_by_id("user_profile_icon").click()
        self.driver.find_element_by_id("iv_login_phone").click()
        self.driver.find_element_by_id("tv_login_with_account").click()
        self.driver.find_element_by_id("login_account").send_keys("832389898@qq.com")
        self.driver.find_element_by_id("login_password").send_keys("832389898@qq.com")
        self.driver.find_element_by_id("button_next").click()
        assert "请求太频繁" in self.driver.page_source



    def test_uiautomator(self):
        # 点击滑动后的views
        self.driver.find_element_by_android_uiautomator('new UiScrollable('
                                                        'new UiSelector().scrollable(true).instance(0))'
                                                        '.scrollIntoView('
                                                        'new UiSelector().text("Views").instance(0)))').click()

        # 点击滑动后的webviews
        self.driver.find_element_by_android_uiautomator('new UiScrollable('
                                                        'new UiSelector().scrollable(true).instance(0))'
                                                        '.scrollIntoView('
                                                        'new UiSelector().text("WebView").instance(0)))').click()

        size = self.driver.get_window_size()
        width = size['width']
        heigth = size['heigth']
        # 从右下滑倒左上,1000代表时间
        self.driver.swipe(width * 0.8, heigth * 0.8, width * 0.1, heigth * 0.1, 1000)

        for i in range(5):
            self.driver.swipe(width * 0.8, heigth * 0.8, width * 0.1, heigth * 0.1, 1000)

    @pytest.mark.parametrize("keyword, stock_type, expect_price",[
        ('alibaba', 'BABA', 100),
        ('xiaomi', '01810', 8.1)
    ])
    def test_search1(self, keyword, stock_type, expect_price):
        self.driver.find_element(By.ID, "home_search").click()
        self.driver.find_element(By.ID,"search_input_text").send_keys(keyword)
        self.driver.find_element_by_id("name").click()
        price = float(self.driver.find_element_by_xpath(
            "//*[contains(@resource-id, 'stockCode') and @text = '"+ stock_type +"']/../../.."
            "//*[contains(@resource-id, 'current_price')]"
        ).text)
        assert price > expect_price