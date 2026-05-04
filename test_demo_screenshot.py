import pytest
from selenium import webdriver
from login_page import LoginPage

def test_login_fallido(driver):
    """Prueba de usuario bloqueado - PASA"""
    driver.get("https://saucedemo.com")
    login = LoginPage(driver)
    login.ingresar_credenciales("locked_out_user", "secret_sauce")
    login.click_login()
    assert "locked out" in login.obtener_error()

def test_login_exitoso(driver):
    """Prueba de login correcto - PASA"""
    driver.get("https://saucedemo.com")
    login = LoginPage(driver)
    login.ingresar_credenciales("standard_user", "secret_sauce")
    login.click_login()
    assert "inventory.html" in driver.current_url

def test_login_con_credenciales_incorrectas(driver):
    """Prueba que FALLA intencionalmente para demostrar screenshot"""
    driver.get("https://saucedemo.com")
    login = LoginPage(driver)
    login.ingresar_credenciales("usuario_invalido", "password_incorrecto")
    login.click_login()
    # Esta aserción fallará intencionalmente para capturar screenshot
    assert "inventory.html" in driver.current_url, "Login debería haber fallado pero se esperaba éxito"
