#study
#https://www.google.com/search?q=playwright+select+option+by+text&sxsrf=ALiCzsYFL8nHSCRQk5MjW0yPTT_PZ9Lrkg%3A1653005840184&ei=EN6GYvbzCsiM5OUPqq6sgAc&oq=playwright+select+by+text&gs_lcp=Cgdnd3Mtd2l6EAMYATIFCAAQywEyBggAEB4QFjIGCAAQHhAWMgYIABAeEBY6BAgjECc6CAgAEB4QFhAKOgUIABCABDoHCAAQChDLAUoECEEYAEoECEYYAFDYBVicGGCcKGgBcAB4AIABpgGIAb8KkgEDMC45mAEAoAEBwAEB&sclient=gws-wiz#kpvalbx=_hN6GYrmrPKOG5OUP85OHwAk16
#https://playwright.dev/docs/selectors#text-selector
#https://medium.com/@jaredpotter1/connecting-puppeteer-to-existing-chrome-window-8a10828149e0
#https://stackoverflow.com/questions/63243137/devtools-remote-debugging-at-chrome-not-working-normally-with-headless-chrome
#https://github.com/microsoft/playwright-python/issues/183
from pathlib import Path
from time import sleep
from playwright.sync_api import sync_playwright

pp =  sync_playwright().start()
browser = pp.chromium.launch(headless=False,executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe")
#browser = pp.chromium.connect("ws://127.0.0.1:9222/devtools/page/D87E9C88ACA17B5406DD31C483493370",timeout=0)
page =browser.new_page(accept_downloads=True,color_scheme="dark")#,user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61/63 Safari/537.36')
#acessar link

#page.context.clear_cookies()

#page.wait_for_timeout(timeout=0)

page.goto('http://www.energisa.com.br',timeout=0)

#page.goto('https://www.youtube.com/')

#selecionar estado
page.locator("#s2id_ddlEstado").click(timeout=0)
page.fill('#s2id_autogen1_search', "MT")
page.keyboard.press('Enter')

#selecionar cidade
page.locator("#s2id_ddlCidade").click()
page.fill('#s2id_autogen2_search', "CUIABA")
page.keyboard.press('Enter')
# bucar
page.locator(".lnkEnviar").click()
page.locator("#s4-titlerow .menu-area").click()

#preencher CNPJ e senha
page.fill('input[id="ctl00_ctl47_g_d885822f_e694_4dbe_b5f3_bcf8d9627447_txtCnpj"]', "19.340.943/0001-91")
page.fill('input[id="ctl00_ctl47_g_d885822f_e694_4dbe_b5f3_bcf8d9627447_txtSenhaCnpj"]', "ose20201")
page.click('#ctl00_ctl47_g_d885822f_e694_4dbe_b5f3_bcf8d9627447_lnkLoginCnpj')
page.locator('.fechar').click()

#mais informações
page.locator("#ctl00_g_1704ddbc_0457_41d9_abe9_f050eb325ff7_agenciaImoveis").click()

#selecionar UC
page.locator(".mais-informacoes ul li:has-text('6/2908091-8')").first.locator(".botao").click()

#clicar botao baixar boleto 
sleep(1)
page.locator(".suaFatura > li:nth-of-type(1) > a img[alt='Extrato e Segunda Via da Conta']").first.click()

#selecionar baixar boleto


sleep(10)
with page.expect_download() as download_info:
        #page.click("text=Extra Small File 5 MB A high quality 5 minute MP3 music file 30secs @ 2 Mbps 10s >> img")
        page.locator("tr:has-text('05/2022')").locator("img[alt='Download']").click()
        #print(page.locator("tr td:has-text('05/2022')").first.inner_text)
        #page.locator("tr:has-text('05/2022')").first.locator("img[alt='Download']").click()

download = download_info.value
print(download.suggested_filename)
#download.save_as(download.suggested_filename)
download.save_as("arquivo_diretorDownload.pdf")

"""sleep(3)
browser.close()
pp.stop()
"""


'''# Interact with login form
#page.click('text=Login')
page.locator("#s2id_ddlEstado .select2-choice").click()
page.fill('input[name="login"]', USERNAME)
page.fill('input[name="password"]', PASSWORD)
page.click('text=Submit')
# Verify app is logged in
'''


#<a class="fechar" href="#fechar" title="Fechar esta janela">Fechar [x]</a>

#/html//div[@id='s4-titlerow']/header[@class='topo']/div[@class='opcoes-usuario']/div[@class='opcoes-navegacao']/div[@class='limites']/div[@class='dados-acesso']/div//nav/ul/li[1]/div//ul