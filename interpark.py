import easyocr
import time
import pyautogui
import chromedriver_autoinstaller
import subprocess
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException


class interpark:
    def __init__(self, seat_max):
        self.driver = None
        self.seat_sel = 0
        self.seat_max = seat_max
        self.map_string = ''
        self.maps = None
        self.l = 0
        self.breaker = False

    def start_interpark(self):
        try:
            shutil.rmtree(r"c:\chrometemp")  # 쿠키 / 캐쉬파일 삭제
        except FileNotFoundError:
            pass

        subprocess.Popen(
            r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

        option = Options()
        option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        try:
            self.driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
        except:
            chromedriver_autoinstaller.install(True)
            self.driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
        self.driver.implicitly_wait(10)

        # 사이즈조절
        self.driver.set_window_size(1400, 1000)
        self.driver.get('https://ticket.interpark.com/Gate/TPLogin.asp')

        # 삭제해야 되는 부분
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
        userId = self.driver.find_element(By.ID, 'userId')
        userId.send_keys('kbyms104')
        userPwd = self.driver.find_element(By.ID, "userPwd")
        userPwd.send_keys('ghkdwp131!')
        userPwd.send_keys(Keys.ENTER)
        # 삭제해야 되는 부분//

    def reservation(self):
        # try:
        #     # 팝업창 닫기 없을 수도 있어서
        #     self.element_click("//*[@id='popup-prdGuide']/div/div[3]/button")
        # except:
        #     print("닫기 할게 없음")
        # # 예매하기 버튼 선택
        # self.element_click("//*[@id='productSide']/div/div[2]/a[1]")
        # # 새창으로 포커스 이동
        # time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        #
        # time.sleep(1)
        # pyautogui.press('enter')
        # time.sleep(2)

        # 미니맵 있냐 없냐 체크해서 돌려돌려 돌림판 좌석 선택까지
        self.map_fork(self.small_map_chk())

        # 좌석선택완료버튼 클릭
        self.element_click("//*[@id='NextStepImage']")

        # 원래 팝업 프레임으로 돌아가기
        self.s_default_content()
        self.s_frame("//*[@id='ifrmBookStep']")

        time.sleep(1)
        # 가격 선택
        basic_price = self.find_elements("//*[contains(@id, 'PriceRow')]/td[3]/select[contains(@pricegradename,'일반')]")

        for p in basic_price:
            s = Select(p)
            s.select_by_index(len(s.options) - 1)

        # 원래 팝업 프레임으로 돌아가기
        self.s_default_content()
        # 다음단계 클릭
        self.element_click("//*[@id='SmallNextBtnImage']")
        time.sleep(1)

        # 예매자 생년월일 입력
        self.s_frame("//*[@id='ifrmBookStep']")
        YYMMDD = self.driver.find_element(By.ID, "YYMMDD")
        YYMMDD.send_keys('900131')

        # 원래 팝업 프레임으로 돌아가기
        self.s_default_content()
        # 다음단계 클릭
        self.element_click("//*[@id='SmallNextBtnImage']")

        # 무통장입금 클릭
        self.s_frame("//*[@id='ifrmBookStep']")
        self.element_click("//*[@id='Payment_22004']/td/label")

        # 은행 선택
        bank_sel = Select(self.driver.find_element(By.XPATH, "//*[@id='BankCode']"))
        bank_sel.select_by_index(1)

        # 원래 팝업 프레임으로 돌아가기
        self.s_default_content()
        # 다음단계 클릭
        self.element_click("//*[@id='SmallNextBtnImage']")

        # 결제하기 수수료 동의하기
        self.s_frame("//*[@id='ifrmBookStep']")
        self.element_click("//*[@id='formConfirm']/div[1]/div/div[1]/div[2]/ul/li[1]/label")
        # 결제하기 클릭
        self.element_click("//*[@id='LargeNextBtnImage']")

    def small_map_chk(self):
        self.s_frame("//*[@id='ifrmSeat']")
        self.s_frame("//*[@id='ifrmSeatView']")

        # 미니맵 종류 구분
        map_string = ""
        flag = True
        try:
            # 미니맵 갯수
            map_string = "//*[@id='TmgsTable']/tbody/tr/td/map"
            self.find_element(map_string)
        except NoSuchElementException as e1:
            try:
                map_string = "//*[@id='TmgsTable']/tbody/tr/td/table/tbody/tr/td/map"
                self.find_element(map_string)
            except NoSuchElementException as e2:
                flag = False

        if flag:
            self.maps = self.find_elements(map_string + "/area")
            self.l = len(self.maps) + 1
        return flag, map_string

    def map_fork(self, flag, map_string):
        # 원래 팝업 프레임으로 돌아가기
        self.s_default_content()
        self.s_frame("//*[@id='ifrmSeat']")

        # 날짜 시간 회차 반복
        # 날짜 포문
        days = Select(self.find_element("//*[@id='PlayDate']"))
        # 날짜 옵션 갯수
        d_op = days.options
        day_cnt = len(d_op)
        # 일자 선택
        for day in range(1, day_cnt):
            days.select_by_index(day)

            # 시간 포문
            times = Select(self.find_element("//*[@id='PlaySeq']"))
            # 시간 옵션 갯수
            t_op = times.options
            time_cnt = len(t_op)
            # 시간 선택
            for t in range(1, time_cnt):
                time.sleep(1)
                times.select_by_index(t)
                time.sleep(1)

                if flag:
                    self.minimap_set(map_string)
                else:
                    self.no_minimap_set()

                if self.breaker:
                    break
                # 원래 팝업 프레임으로 돌아가기
                self.s_default_content()
                self.s_frame("//*[@id='ifrmSeat']")

            # 원래 팝업 프레임으로 돌아가기
            self.s_default_content()
            self.s_frame("//*[@id='ifrmSeat']")
            if self.breaker:
                break

    # 미니맵이 1단계만 있는 공연
    def minimap_set(self, map_string):
        self.no_minimap_set()

        # 미니맵 갯수만큼 포문 돌리기
        for i in range(2, self.l):
            # 원래 팝업 프레임으로 돌아가기
            # 미니맵 iframe을 이동
            self.s_default_content()
            self.s_frame("//*[@id='ifrmSeat']")
            self.s_frame("//*[@id='ifrmSeatView']")

            # 맵 순서가 지멋대로라서 href 에 있는 RGN 체크 해서 선택하기.
            try:
                self.element_click(map_string + "/area[contains(@onmouseover,'RGN00" + str(i) + "')]")
            except:
                break
            self.no_minimap_set()
            if self.breaker:
                break

    # 미니맵이 없는 공연
    def no_minimap_set(self):
        # 원래 팝업 프레임으로 돌아가기
        # 좌석 iframe으로 이동
        self.s_default_content()
        self.s_frame("//*[@id='ifrmSeat']")
        self.s_frame("//*[@id='ifrmSeatDetail']")
        # 활성화되있는 시트 불러오기
        seats = self.find_css("img.stySeat")

        # 좌석 선택
        if len(seats) > 0:
            for seat in seats:
                seat.click()
                self.seat_sel = self.seat_sel + 1
                # 시트선택된 갯수가 최대선택시트 갯수 이상이 될 경우 선택 중지
                if self.seat_sel >= self.seat_max:
                    self.breaker = True
                    break

    def s_default_content(self):
        self.driver.switch_to.default_content()

    def s_frame(self, xpath):
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, xpath))

    def element_click(self, xpath):
        self.driver.find_element(By.XPATH, xpath).click()

    def find_css(self, selector):
        self.driver.find_elements(By.CSS_SELECTOR, selector)

    def find_element(self, xpath):
        self.driver.find_element(By.XPATH, xpath)

    def find_elements(self, xpath):
        return self.driver.find_element(By.XPATH, xpath)

