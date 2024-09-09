import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])


class Driver:
    def __init__(self):
        self.__url = 'https://www.zhipin.com/web/user/?ka=header-login'
        self.__driver = webdriver.Chrome(options=options)
        self.__worklist = []
        self.__page_dict = {}

    def run(self):

        self.__driver.get(self.__url)
        self.wait_for_keypress()
        self.__wait(1)
        self.do_click('//*[@id="header"]/div[1]/div[2]/ul/li[1]/a')
        self.__wait(1)
        self.do_input('//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/div[2]/p/input', self.__kw)
        self.__wait(1)
        self.do_click('//*[@id="wrap"]/div[3]/div/div[1]/div[1]/form/button')
        self.__wait(3)
        self.get_work_list()
        self.__wait(2)
        self.do_send_msg()

    def wait_for_keypress(self):
        self.__kw = input("【请完成登陆后】输入需要搜索工作之关键字：")
        self.to_send_words = input("请输入需要给boss的问候语：")

    def do_send_msg(self):
        for k, v in self.__page_dict.items():
            for index, item in enumerate(v):
                self.__driver.get(url=item)
                time.sleep(1)
                start_tag = WebDriverWait(self.__driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/div[1]/div/div/div/div[3]/div[1]/a[2]'))
                )
                text = start_tag.text
                if text == "继续沟通":
                    print("这个页面已沟通！")
                    # continue
                else:
                    # 执行点击事件
                    try:
                        start_tag.click()
                        time.sleep(1)
                        try:  # /html/body/div[11]/div[2]/div[2]/div/div[2]/div[2]/div[3]/button
                            login_btn_tag = WebDriverWait(self.__driver, 0.5).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '/html/body/div[11]/div[2]/div[2]/div/div[2]/div[2]/div[3]/button'))
                            )
                            t = input("登录成功后输入任意值按回车继续")
                        except:
                            print("已登录")
                        print(1121)
                        textarea_tag = WebDriverWait(self.__driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '/html/body/div[11]/div[2]/div[2]/div/div[1]/div[2]/textarea'))
                        )
                        textarea_tag.send_keys(self.to_send_words)
                        sendbtn_tag = WebDriverWait(self.__driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '/html/body/div[11]/div[2]/div[2]/div/div[1]/div[2]/div'))
                        )
                        sendbtn_tag.click()

                    except Exception as e:
                        # 这里显然就是进入chat页面
                        # //*[@id="chat-input"]
                        try:
                            # div_input_tag = WebDriverWait(self.__driver, 10).until(
                            #     EC.element_to_be_clickable(
                            #         (By.XPATH, '//div[@id="chat-input"]'))
                            # )
                            # print("标签")
                            # self.__driver.execute_script("arguments[0].innerText = arguments[1];", div_input_tag,
                            #                              self.to_send_words)
                            #
                            # do_submit_btn_tag = WebDriverWait(self.__driver, 10).until(
                            #     EC.element_to_be_clickable(
                            #         (By.XPATH, '//*[@id="container"]/div/div/div[2]/div[3]/div/div[3]/button'))
                            # )
                            # do_submit_btn_tag.click()

                            btn1_tag = WebDriverWait(self.__driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH,
                                     '//*[@id="container"]/div/div/div[2]/div[3]/div/div[1]/div[2]'))
                            )
                            btn1_tag.click()
                            print(11)
                            li_tag = WebDriverWait(self.__driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH,
                                     '//*[@id="container"]/div/div/div[2]/div[3]/div/div[5]/ul/li[1]'))
                            )
                            # //*[@id="container"]/div/div/div[2]/div[3]/div/div[5]/ul/li[1]
                            li_tag.click()
                        except:
                            print("xxx错!")

                print("item", item)

    def get_work_list(self):

        page_tag_list = WebDriverWait(self.__driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="wrap"]/div[2]/div[2]/div/div[1]/div[2]/div/div/div/a'))
        )
        num = len(page_tag_list)
        page_url_list = [self.__driver.current_url + f"&page={x}" for x in range(1, num + 1)]
        print("page_url_list", page_url_list)
        for index, page_url in enumerate(page_url_list):
            self.__page_dict[index] = []
            self.__driver.get(page_url)
            time.sleep(1)
            print("页面链接导入成功！")
            ul_tag = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@class="job-list-box"]'))
            )
            li_elements = ul_tag.find_elements(By.XPATH, './li')
            for li in li_elements:
                a_tag = li.find_element(By.XPATH, './div[1]/a[1]')
                href = a_tag.get_attribute('href')
                work_url = href
                self.__page_dict[index].append(work_url)
            print(self.__page_dict[index])

    def do_click(self, xpath_str):
        try:
            tag = WebDriverWait(self.__driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_str))
            )
            tag.click()
        except Exception as e:
            print(f"Error while clicking: {e}")

    def do_input(self, xpath_str, kw):
        try:
            input_tag = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_str))
            )
            input_tag.send_keys(kw)
        except Exception as e:
            print(f"Error while inputting text: {e}")

    def __wait(self, t):
        time.sleep(t)

    def close(self):
        self.__driver.quit()


if __name__ == '__main__':
    obj = Driver()
    obj.run()
