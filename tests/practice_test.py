import pytest
from selenium import webdriver;
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


class Item():
    def __init__(self, name, driver):
        self.element = driver.find_element(By.XPATH, f"//h6[text()='{name}']/..")
        self.name = self.element.find_element(By.TAG_NAME, "h6").text;
        self.quantity = 0;
        self.price = self.get_price(self.element);
        # print(self.name + " " + self.price + " " + str(len(self.element.find_elements(By.XPATH, "./*"))) );
    def check_if_addable(self):
        try:
            self.element.find_element(By.XPATH, "./div/button[text()='Add to Cart']");
            return True;
        except:
            return False;
    def add_to_cart(self):
        if(self.check_if_addable()):
            add = self.element.find_element(By.XPATH, "./div/button[text()='Add to Cart']");
            add.click();
        else:
            print("cannot add to cart")
    def increase(self):
        if(self.check_if_addable()):
            return;
        inc = self.element.find_elements(By.XPATH, "./*")[3].find_elements(By.TAG_NAME, 'button')[1];
        inc.click();
    def decrease(self):
        if(self.check_if_addable()):
            return;
        dec = self.element.find_elements(By.XPATH, "./*")[3].find_elements(By.TAG_NAME, 'button')[0];
        dec.click();
    def remove(self):
        if(self.check_if_addable()):
            return;
        quantity = self.get_quantity()
        dec = self.element.find_elements(By.XPATH, "./*")[3].find_elements(By.TAG_NAME, 'button')[0];
        for i in range(quantity):
            dec.click();
    def get_quantity(self):
        if(self.check_if_addable()):
            return 0;
        qty = self.element.find_elements(By.XPATH, "./*")[3].find_element(By.TAG_NAME, 'p');
        self.quantity = int(qty.text);
        return self.quantity;
    def get_price(self, element):
        price_element = element.find_element(By.XPATH, f".//p[text()='$']");
        return int(price_element.text.replace("$",""));

class ShoppingCart():
    def __init__(self, name, driver):
        self.element = driver.find_element(By.XPATH, f"//p[text()='{name}']/..")
        self.name = name
        self.price = self.get_price()
    def increase(self):
        inc = self.element.find_elements(By.XPATH, "./*")[1].find_elements(By.TAG_NAME, 'button')[1];
        inc.click();
    def decrease(self):
        dec = self.element.find_elements(By.XPATH, "./*")[1].find_elements(By.TAG_NAME, 'button')[0];
        dec.click();
    def remove(self):
        qty = self.element.find_elements(By.XPATH, "./*")[1].find_element(By.TAG_NAME, 'p');
        dec = self.element.find_elements(By.XPATH, "./*")[1].find_elements(By.TAG_NAME, 'button')[0];
        for i in range(int(qty.text)):
            dec.click();
    def get_quantity(self):
        qty = self.element.find_elements(By.XPATH, "./*")[1].find_element(By.TAG_NAME, 'p');
        return int(qty.text);
    def get_price(self):
        price_element = self.element.find_element(By.TAG_NAME, "p");
        price = price_element.text.split("$")[1].replace(")","");
        return int(price);
    def get_total_price(self):
        price = self.element.find_elements(By.XPATH, "./*")[2];
        return int(price.text.replace("$",""));

class TestCheckout():
    chrome_options = Options();
    # prefs = {"credentials_enable_service": False,
    #         "profile.password_manager_enabled": False,
    #         "profile.password_manager_leak_detection": False}
    # chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_experimental_option("detach", True);

    driver = webdriver.Chrome(options=chrome_options);
    driver.get("https://www.cnarios.com/challenges/product-purchasing#challenge");
    # driver = webdriver.Chrome();
    # driver.implicitly_wait(5);
    @pytest.fixture
    def refresh(self):
        self.driver.refresh();
    
    def goto_payment(self):
        item = Item("Laptop Backpack", self.driver);
        item.add_to_cart();
        cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        cart.click();
        checkout = self.driver.find_element(By.XPATH, '//button[text()="Proceed to Address"]');
        checkout.click();
        first_name = self.driver.find_element(By.XPATH, "//label[text()='First Name']/following-sibling::div/input");
        last_name = self.driver.find_element(By.XPATH, "//label[text()='Last Name']/following-sibling::div/input");
        address = self.driver.find_element(By.XPATH, "//label[text()='Address']/following-sibling::div/textarea");
        first_name.send_keys("John");
        last_name.send_keys("Doe");
        address.send_keys("123 Main St");
        payment_button = self.driver.find_element(By.XPATH, '//button[text()="Proceed to Payment"]');
        payment_button.click();
    # @pytest.mark.skip(reason="skipping")
    def ui_path(self):
        nav = self.driver.find_elements(By.CLASS_NAME, 'MuiStepLabel-iconContainer');
        cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        anchor_pointer = cart.find_element(By.CLASS_NAME, 'MuiBadge-anchorOriginTopRight')
        assert "MuiBadge-invisible" in anchor_pointer.get_attribute("class");
        assert len(nav) == 5;
        assert "Mui-active" in nav[0].get_attribute("class")
        assert "1" in nav[0].find_element(By.TAG_NAME, "text").text;
        assert "2" in nav[1].find_element(By.TAG_NAME, "text").text;
        assert "Mui-disabled" in nav[1].get_attribute("class")
        item = Item("Laptop Backpack", self.driver);
        item.add_to_cart();
        assert "1" == anchor_pointer.text;
        cart.click();
        assert "Mui-complete" in nav[0].get_attribute("class")
        assert "Mui-active" in nav[1].get_attribute("class")
        assert "2" in nav[1].find_element(By.TAG_NAME, "text").text;
        assert "3" in nav[2].find_element(By.TAG_NAME, "text").text;
        assert "Mui-disabled" in nav[2].get_attribute("class")
        checkout = self.driver.find_element(By.XPATH, '//button[text()="Proceed to Address"]');
        checkout.click();
        assert "Mui-complete" in nav[1].get_attribute("class")
        assert "Mui-active" in nav[2].get_attribute("class")
        assert "3" in nav[2].find_element(By.TAG_NAME, "text").text;
        assert "4" in nav[3].find_element(By.TAG_NAME, "text").text;
        assert "Mui-disabled" in nav[3].get_attribute("class")
        first_name = self.driver.find_element(By.XPATH, "//label[text()='First Name']/following-sibling::div/input");
        last_name = self.driver.find_element(By.XPATH, "//label[text()='Last Name']/following-sibling::div/input");
        address = self.driver.find_element(By.XPATH, "//label[text()='Address']/following-sibling::div/textarea");
        first_name.send_keys("John");
        last_name.send_keys("Doe");
        address.send_keys("123 Main St");
        payment_button = self.driver.find_element(By.XPATH, '//button[text()="Proceed to Payment"]');
        payment_button.click();
        assert "Mui-complete" in nav[2].get_attribute("class")
        assert "Mui-active" in nav[3].get_attribute("class")
        assert "4" in nav[3].find_element(By.TAG_NAME, "text").text;
        assert "5" in nav[4].find_element(By.TAG_NAME, "text").text;
        assert "Mui-disabled" in nav[4].get_attribute("class")
        return nav;
    def test_item(self, refresh):
        self.driver.refresh()
        item = Item("Laptop Backpack", self.driver);
        item.add_to_cart();
        # cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        # cart.click();
        item.increase();
        item.increase();
        item.decrease();
        item.get_quantity();
        item.remove();

    # @pytest.mark.skip(reason="skipping")
    @pytest.mark.parametrize("item_name", [
        ("Laptop Backpack"),
        ("Fitness Band"),
        ("Wireless Headphones"),
        ("Bluetooth Speaker"),
        ])
    def test_adding_and_removing_func(self, item_name, refresh):
        self.driver.refresh()
        cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        item = Item(item_name, self.driver);
        item.add_to_cart();
        badge = cart.find_element(By.CLASS_NAME, 'MuiBadge-anchorOriginTopRight');
        assert item.get_quantity() == 1;
        assert "1" == badge.text;
        item.remove();
        assert item.get_quantity() == 0;
        assert "MuiBadge-invisible" in badge.get_attribute("class");
    
    # @pytest.mark.skip(reason="skipping")
    def test_correct_cart_number(self, refresh):
        self.driver.refresh()
        cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        items = ["Laptop Backpack", "Fitness Band", "Wireless Headphones", "Bluetooth Speaker"];
        badge = cart.find_element(By.CLASS_NAME, 'MuiBadge-anchorOriginTopRight');
        for i in range(len(items)):
            item = Item(items[i], self.driver);
            item.add_to_cart();
            assert item.get_quantity() == 1;
            assert str(i+1) == badge.text;
        for i in range(len(items)):
            item = Item(items[i], self.driver);
            item.remove();
            assert item.get_quantity() == 0;
            if(i < len(items) - 1):
                assert str(len(items) - i - 1) == badge.text;
            else:
                assert "MuiBadge-invisible" in badge.get_attribute("class");
    
    # @pytest.mark.skip(reason="skipping")
    @pytest.mark.parametrize("item_name, volume", [
        ("Fitness Band",10),
        ("Wireless Headphones",5),
        ("Bluetooth Speaker",3),
        ("Laptop Backpack",7),
    ])
    def test_increase_decrease(self, item_name, volume, refresh):
        self.driver.refresh()
        item = Item(item_name, self.driver);
        item.add_to_cart();
        for i in range(volume-1):
            item.increase();
        assert item.get_quantity() == volume;
        for i in range(volume-1):
            item.decrease();
        assert item.get_quantity() == 1;
        item.decrease();
        assert item.get_quantity() == 0;

# check to see if added items appear in cart with correct quantities
    # @pytest.mark.skip(reason="skipping")
    def test_cart_values(self, refresh):
        self.driver.refresh()
        items = [("Laptop Backpack",2), ("Fitness Band",3), ("Wireless Headphones",1), ("Bluetooth Speaker",4)];
        check_items = [];
        for i in range(len(items)):
            item = Item(items[i][0], self.driver);
            check_items.append(item);
            item.add_to_cart();
            for i in range(1, items[i][1]):
                item.increase();
        cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        cart.click();
        total = 0;
        for i in range(len(items)):
            shopping = ShoppingCart(items[i][0], self.driver);
            assert shopping.price == check_items[i].price;
            assert shopping.get_quantity() == items[i][1];
            assert shopping.price * items[i][1] == shopping.get_total_price();
            total += shopping.price * items[i][1];
        assert str(total) == self.driver.find_element(By.XPATH, '//h6[contains(text(),"Total:")]').text.split("$")[1];

    # @pytest.mark.skip(reason="skipping")
    def test_increase_and_removal_in_cart(self, refresh):
        self.driver.refresh()
        items = [("Laptop Backpack",2), ("Fitness Band",3), ("Wireless Headphones",1), ("Bluetooth Speaker",4)];
        for i in range(len(items)):
            item = Item(items[i][0], self.driver);
            item.add_to_cart();
            for j in range(1, items[i][1]):
                item.increase();
        cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        cart.click();
        total_pointer = self.driver.find_element(By.XPATH, '//h6[contains(text(),"Total:")]')
        total = int(total_pointer.text.split("$")[1]);
        for i in range(len(items)):
            print(items[i][1])
            shopping = 0;
            shopping = ShoppingCart(items[i][0], self.driver);
            assert items[i][0] in shopping.element.find_element(By.TAG_NAME,"p").text
            assert shopping.get_quantity() == items[i][1]
            for j in range(4):
                shopping.increase();
            assert shopping.get_quantity() == items[i][1] + 4;
            assert shopping.price * shopping.get_quantity() == shopping.get_total_price();
            assert total + (4 * shopping.price) == int(total_pointer.text.split("$")[1]);
            total += 4 * shopping.price;
            shopping.decrease();
            assert shopping.get_quantity() == items[i][1] + 3;
            assert shopping.price * shopping.get_quantity() == shopping.get_total_price();
            assert total - shopping.price == int(total_pointer.text.split("$")[1]);
            total -= shopping.price;

            anchor_pointer = cart.find_element(By.CLASS_NAME, 'MuiBadge-anchorOriginTopRight')
            before = cart.find_element(By.CLASS_NAME, 'MuiBadge-anchorOriginTopRight').text;
            total-= shopping.price * shopping.get_quantity();
            shopping.remove();
            if(before == "1"):
                assert "MuiBadge-invisible" in anchor_pointer.get_attribute("class");
            else:
                assert int(anchor_pointer.text) == int(before) - 1;
            try:
                shopping = ShoppingCart(item[i][0], self.driver);
            except:
                print("passed")
            
        assert total == 0;

    def test_form(self, refresh):
        item = Item("Laptop Backpack", self.driver);
        item.add_to_cart();
        cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        cart.click();
        checkout = self.driver.find_element(By.XPATH, '//button[text()="Proceed to Address"]');
        checkout.click();
        first_name = self.driver.find_element(By.XPATH, "//label[text()='First Name']/following-sibling::div/input");
        last_name = self.driver.find_element(By.XPATH, "//label[text()='Last Name']/following-sibling::div/input");
        address = self.driver.find_element(By.XPATH, "//label[text()='Address']/following-sibling::div/textarea");
        payment_button = self.driver.find_element(By.XPATH, '//button[text()="Proceed to Payment"]');
        assert payment_button.is_enabled() == False;
        first_name.send_keys("John");
        assert payment_button.is_enabled() == False;
        last_name.send_keys("Doe");
        assert payment_button.is_enabled() == False;
        address.send_keys("123 Main St");
        assert payment_button.is_enabled() == True;
        payment_button.click();

    def test_payment_pass_and_total(self, refresh):
        self.goto_payment();
        pay_button = self.driver.find_element(By.XPATH, '//button[text()="Pay Now"]');
        pay_button.click();
        success_msg = self.driver.find_element(By.XPATH, '//h5[text()="🎉 Order Placed Successfully!"]');
        assert success_msg.is_displayed();
    
    def test_payment_fail(self, refresh):
        self.goto_payment();
        cancel_button = self.driver.find_element(By.XPATH, '//button[text()="Cancel"]');
        cancel_button.click();
        error_msg = self.driver.find_element(By.XPATH, '//h6[text()="❌ Payment Failed!"]');
        assert error_msg.is_displayed();

    def test_empty_cart(self, refresh):
        cart = self.driver.find_element(By.XPATH, '//h6[text()="My Shop"]/following-sibling::button');
        cart.click();
        empty_msg = self.driver.find_element(By.XPATH, '//button[text()="Proceed to Address"]');
        assert empty_msg.is_enabled() == False;

    def test_ui_path_and_home_reset(self, refresh):
        nav = self.ui_path();
        pay_button = self.driver.find_element(By.XPATH, '//button[text()="Pay Now"]');
        pay_button.click();
        assert "Mui-complete" in nav[3].get_attribute("class")
        # bug here, should be complete not active and have check mark
        try:
            assert "Mui-complete" in nav[4].get_attribute("class")
            assert "Mui-active" not in nav[4].get_attribute("class")
        except:
            print("payment successful but marked unsuccessful in ui")
            raise
        assert "Mui-active" in nav[4].get_attribute("class")
        assert "Mui-complete" not in nav[4].get_attribute("class")
        home = self.driver.find_element(By.XPATH, '//button[text()="Back to Home"]');
        home.click();
        nav = self.ui_path();
        cancel_button = self.driver.find_element(By.XPATH, '//button[text()="Cancel"]');
        cancel_button.click();
        assert "Mui-complete" in nav[3].get_attribute("class")
        # success gets marks complete here where it shouldnt be
        try:
            assert "Mui-active" in nav[4].get_attribute("class")
            assert "Mui-complete" not in nav[4].get_attribute("class")
            assert "5" in nav[4].find_element(By.TAG_NAME, "text").text;
        except:
            print("payment unsuccessful but marked successful in ui")
            raise