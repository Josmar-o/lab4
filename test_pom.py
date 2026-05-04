from selenium import webdriver
from login_page import LoginPage

def test_ejecucion_pom():
    driver = webdriver.Chrome()
    driver.get("https://saucedemo.com")
    login = LoginPage(driver)
    
    # Caso de Uso: Login Fallido
    login.ingresar_credenciales("locked_out_user", "secret_sauce")
    login.click_login()
    mensaje = login.obtener_error()
    print(f"Resultado de la prueba: {mensaje}")
    driver.quit()

if __name__ == "__main__":
    test_ejecucion_pom()
