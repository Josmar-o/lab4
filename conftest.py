import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from datetime import datetime

# Crear carpeta de capturas si no existe
CAPTURAS_DIR = "capturas"
if not os.path.exists(CAPTURAS_DIR):
    os.makedirs(CAPTURAS_DIR)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura de pantalla automática siempre (pase o falle)"""
    outcome = yield
    report = outcome.get_result()
    
    # Capturar screenshot siempre cuando se ejecuta el test (call phase)
    if report.when == "call":
        try:
            driver = item.funcargs['driver']
            
            # Determinar el estado del test
            status = "PASSED" if report.passed else "FAILED"
            
            # Crear nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name
            filename = f"{test_name}_{status}_{timestamp}.png"
            filepath = os.path.join(CAPTURAS_DIR, filename)
            
            # Guardar screenshot como archivo PNG
            driver.save_screenshot(filepath)
            print(f"\n📸 Screenshot guardado: {filepath}")
            
            # Obtener screenshot en base64 para el reporte HTML
            screenshot = driver.get_screenshot_as_base64()
            
            # Agregar al reporte HTML con indicador de estado
            color = "green" if report.passed else "red"
            html = f'<div><strong style="color:{color};">{status}</strong><br><img src="data:image/png;base64,{screenshot}" alt="screenshot" style="width:600px;height:auto;" onclick="window.open(this.src)" align="right"/></div>'
            
            # Usar pytest_html.extras para agregar contenido HTML
            import pytest_html
            extra = getattr(report, 'extras', [])
            extra.append(pytest_html.extras.html(html))
            report.extras = extra
            
        except Exception as e:
            print(f"❌ No se pudo tomar screenshot: {e}")

@pytest.fixture
def driver():
    """Fixture del navegador"""
    options = Options()
    # Descomenta la línea de abajo si quieres modo headless (sin ventana):
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=options)
    d.maximize_window()
    yield d
    d.quit()
