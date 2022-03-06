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


try:
    shutil.rmtree(r"c:\chrometemp")  #쿠키 / 캐쉬파일 삭제
except FileNotFoundError:
    pass

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"') # 디버거 크롬 구동

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(10)

# 사이즈조절
driver.set_window_size(1400, 1000)
driver.get('https://ticket.interpark.com/Gate/TPLogin.asp')

driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
userId = driver.find_element(By.ID, 'userId')
userId.send_keys('kbyms104')
userPwd = driver.find_element(By.ID, "userPwd")
userPwd.send_keys('ghkdwp131!')
userPwd.send_keys(Keys.ENTER)

time.sleep(3)
goodsCode = 99999989
driver.get('https://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=' + '22002148')

time.sleep(1)

driver.find_element(By.XPATH, "//*[@id='popup-prdGuide']/div/div[3]/button").click()
driver.find_element(By.XPATH, "//*[@id='productSide']/div/div[2]/a[1]").click()

time.sleep(2)

# 예매하기 눌러서 팝업창이 뜨면 포커스를 새창으로 바꿔준다
driver.switch_to.window(driver.window_handles[1])
#driver.get_window_position(driver.window_handles[1])


# iframe 이동
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))

capchaPng = driver.find_element(By.XPATH, "//*[@id='imgCaptcha']")

reader = easyocr.Reader(['en'])
result = reader.readtext(capchaPng.screenshot_as_png, detail=0)

capchaValue = result[0].replace(' ', '').replace('5', 'S').replace('0', 'O').replace('$', 'S').replace(',', '')\
    .replace(':', '').replace('.', '').replace('+', 'T').replace("'", '').replace('`', '').replace('군', 'Z')\
    .replace('1', 'L').replace('e', 'Q').replace('3', 'S').replace('€', 'C').replace('{', '').replace('-', '')


driver.find_element_by_class_name('validationTxt').click()
chapchaText = driver.find_element_by_id('txtCaptcha')

chapchaText.send_keys(capchaValue)
chapchaText.send_keys(Keys.ENTER)

# 미니맵 iframe
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeatView']"))

# 미니맵 종류 구분
map_string = "//*[@id='TmgsTable']/tbody/tr/td/map"
try:
    # 미니맵 갯수
    driver.find_element(By.XPATH, map_string)
    maps = driver.find_elements(By.XPATH, map_string + "/area")
except NoSuchElementException:
    map_string = "//*[@id='TmgsTable']/tbody/tr/td/table/tbody/tr/td/map"
    maps = driver.find_elements(By.XPATH, map_string + "/area")

l = len(maps) + 1

seat_sel = 0
seat_max = 5

# 원래 팝업 프레임으로 돌아가기
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))

# for문 빠져나가기 변수 선언
breaker = False

# 날짜 포문
days = Select(driver.find_element(By.XPATH, "//*[@id='PlayDate']"))
# 날짜 옵션 갯수
d_op = days.options
day_cnt = len(d_op)
# 일자 선택
for day in range(1, day_cnt):
    days.select_by_index(day)
    time.sleep(1)

    # 시간 포문
    times = Select(driver.find_element(By.XPATH, "//*[@id='PlaySeq']"))
    # 시간 옵션 갯수
    t_op = times.options
    time_cnt = len(t_op)
    # 시간 선택
    for t in range(1, time_cnt):
        time.sleep(1)
        times.select_by_index(t)
        time.sleep(1)
        # 좌석 iframe으로 이동
        driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeatDetail']"))
        # 활성화되있는 시트 불러오기
        seats = driver.find_elements(By.CSS_SELECTOR, "img.stySeat")

        # 시간 선택 하고 나서 처음에 좌석이 있는지 체크
        if len(seats) > 0:
            # 활성화되어있는 시트가 있으면 시트 선택
            for seat in seats:
                seat.click()
                seat_sel = seat_sel + 1
                # 시트선택된 갯수가 최대선택시트 갯수 이상이 될 경우 선택 중지
                if seat_sel >= seat_max:
                    breaker = True
                    break
        if breaker:
            break

        # 미니맵 갯수만큼 포문 돌리기
        for i in range(2, l):
            # 원래 팝업 프레임으로 돌아가기
            # 미니맵 iframe을 이동
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))
            driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeatView']"))

            # 맵 순서가 지멋대로라서 href 에 있는 RGN 체크 해서 선택하기.
            try:
                driver.find_element(By.XPATH, map_string + "/area[contains(@onmouseover,'RGN00" + str(i) + "')]").click()
            except:
                break

            # 원래 팝업 프레임으로 돌아가기
            # 좌석 iframe으로 이동
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))
            driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeatDetail']"))
            # 활성화되있는 시트 불러오기
            seats = driver.find_elements(By.CSS_SELECTOR, "img.stySeat")

            # 좌석 선택
            if len(seats) > 0:
                for seat in seats:
                    seat.click()
                    seat_sel = seat_sel + 1
                    # 시트선택된 갯수가 최대선택시트 갯수 이상이 될 경우 선택 중지
                    if seat_sel >= seat_max:
                        breaker = True
                        break
            if breaker:
                break

        if breaker:
            break
        # 원래 팝업 프레임으로 돌아가기
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))

    # 원래 팝업 프레임으로 돌아가기
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))
    if breaker:
        break

# 좌석 선택하세요 or 이선좌 체크 해줘야 하는 부분

# 좌석선택완료버튼 클릭
driver.find_element(By.XPATH, "//*[@id='NextStepImage']").click()

# 원래 팝업 프레임으로 돌아가기
driver.switch_to.default_content()
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))

time.sleep(1)
# 가격 선택
basic_price = driver.find_elements(By.XPATH, "//*[contains(@id, 'PriceRow')]/td[3]/select[contains(@pricegradename,'일반')]")
for p in basic_price:
    s = Select(p)
    s.select_by_index(len(s.options)-1)


# 원래 팝업 프레임으로 돌아가기
driver.switch_to.default_content()
# 다음단계 클릭
driver.find_element(By.XPATH, "//*[@id='SmallNextBtnImage']").click()

time.sleep(1)

# 예매자 생년월일 입력
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
YYMMDD = driver.find_element(By.ID, "YYMMDD")
YYMMDD.send_keys('900131')

# 원래 팝업 프레임으로 돌아가기
driver.switch_to.default_content()
# 다음단계 클릭
driver.find_element(By.XPATH, "//*[@id='SmallNextBtnImage']").click()


# 무통장입금 클릭
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
driver.find_element(By.XPATH, "//*[@id='Payment_22004']/td/label").click()

# 은행 선택
bank_sel = Select(driver.find_element(By.XPATH, "//*[@id='BankCode']"))
bank_sel.select_by_index(1)

# 원래 팝업 프레임으로 돌아가기
driver.switch_to.default_content()
# 다음단계 클릭
driver.find_element(By.XPATH, "//*[@id='SmallNextBtnImage']").click()

# 결제하기 수수료 동의하기
driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
driver.find_element(By.XPATH, "//*[@id='formConfirm']/div[1]/div/div[1]/div[2]/ul/li[1]/label").click()
# 결제하기 클릭
driver.find_element(By.XPATH, "//*[@id='LargeNextBtnImage']").click()
