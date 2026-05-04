from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    # --- CASO 1: Login Seguro ---
    print("Ejecutando Caso 1: Login Seguro...")
    driver.get("https://saucedemo.com")
    user_input = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    user_input.send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.url_contains("inventory.html"))
    print("✅ Caso 1 completado con éxito.")
    
    # --- CASO 2: Agregar al Carrito con Verificación de Clic ---
    print("Ejecutando Caso 2: Agregar al Carrito...")
    btn_add = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")))
    btn_add.click()
    badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    print(f"✅ Caso 2 completado: Carrito tiene {badge.text} producto(s).")
    
    # --- CASO 3: Validación de Error de Bloqueo ---
    print("Ejecutando Caso 3: Login Fallido...")
    driver.delete_all_cookies()
    driver.get("https://saucedemo.com")
    user_input_locked = wait.until(EC.visibility_of_element_located((By.ID, "user-name")))
    user_input_locked.send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    error_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']")))
    print(f"✅ Caso 3 completado: {error_container.text}")

finally:
    driver.quit()
