
from email import header
from heapq import heapify
from time import sleep
from time import time
from zoneinfo import available_timezones
from playwright.sync_api import sync_playwright
from datetime import timedelta
from fake_headers import Headers

class bot:

    num2mes = {"01":"JAN",
        "02":"FEV",
        "03":"MAR",
        "04":"ABR",
        "05":"MAI",
        "06":"JUN",
        "07":"JUL",
        "08":"AGO",
        "09":"SET",
        "10":"OUT",
        "11":"NOV",
        "12":"DEZ"}
    header = Headers(headers=True)
    inicio = 0
    fim = 0

    def __init__(self,url,tempoEspera):
        self.url = url
        self.asyncPlay = sync_playwright().start()
        self.browser =  self.asyncPlay.chromium.launch(headless=False,channel="chrome")
        #self.context = self.browser.new_context()
        self.logado = False
        self.inicio = time()
        self.tempoEspera = tempoEspera

    def abrirPagina(self):
        headerPag = self.header.generate()
        print("HEADERS FAKE: ")
        print(headerPag)
        self.pagina = self.browser.new_page(accept_downloads=True,extra_http_headers=headerPag)

    def entrarSite(self):
        self.pagina.goto(self.url,timeout=0)
    
    def selecionarUfCidade(self):
        #selecionar estado
        self.pagina.locator("#s2id_ddlEstado").click()
        self.pagina.fill('#s2id_autogen1_search', "MT")
        sleep(self.tempoEspera["rapido"])
        self.pagina.keyboard.press('Enter')

        #selecionar cidade
        self.pagina.locator("#s2id_ddlCidade").click()
        self.pagina.fill('#s2id_autogen2_search', "CUIABA")
        self.pagina.keyboard.press('Enter')
        # bucar
        sleep(self.tempoEspera["rapido"])
        self.pagina.locator(".lnkEnviar").click()
        self.pagina.locator("#s4-titlerow .menu-area").click()

    def fazerLogin(self,user, senha):
        #preencher CNPJ e senha
        self.pagina.fill('input[id="ctl00_ctl47_g_d885822f_e694_4dbe_b5f3_bcf8d9627447_txtCnpj"]',user)
        self.pagina.fill('input[id="ctl00_ctl47_g_d885822f_e694_4dbe_b5f3_bcf8d9627447_txtSenhaCnpj"]', senha)
        self.pagina.click('#ctl00_ctl47_g_d885822f_e694_4dbe_b5f3_bcf8d9627447_lnkLoginCnpj')
        sleep(self.tempoEspera["lento"])
        if self.pagina.locator(".avatar").count()  >=1  and self.pagina.locator(".avatar").is_visible():
            self.logado = True
            print("esperando carregar site...")
        else:
            self.logado = False
 
        
    def selecionarUc(self,uc):
        #sleep(3)
        if self.pagina.locator('.fechar').count() >= 1 and self.pagina.locator('.fechar').is_visible():
            self.pagina.locator('.fechar').click()
        #mais informações
        self.pagina.locator("#ctl00_g_1704ddbc_0457_41d9_abe9_f050eb325ff7_agenciaImoveis").click()
        #selecionar UC
        if self.pagina.locator(".mais-informacoes ul li:has-text('" + uc + "')").first.locator(".botao").count() >= 1:
            self.pagina.locator(".mais-informacoes ul li:has-text('" + uc + "')").first.locator(".botao").click()
            return 1
        else:
            print("UC não encontrada")
            return 0
    
    def fazerDownload(self,nomeArquivo,mesAno):
        print("tentando baixar...")
        sleep(self.tempoEspera["medio"])
        if self.pagina.locator("(//div[@class='tabela-imoveis']//thead)[2]").count() <= 0:
            self.pagina.locator(".suaFatura > li:nth-of-type(1) > a img[alt='Extrato e Segunda Via da Conta']").first.click(timeout=0)
        sleep(self.tempoEspera["medio"])
        if self.pagina.locator("(//div[@class='tabela-imoveis']//thead)[2]").count() >= 1:
            if self.pagina.locator("tr:has-text('" + self.getMes(mesAno) + "')").locator("img[alt='Download']").count() >= 1:
                with self.pagina.expect_download() as download_info:
                    self.pagina.locator("tr:has-text('" + self.getMes(mesAno) + "')").locator("img[alt='Download']").click()
                download = download_info.value
                download.save_as( nomeArquivo + ".pdf")
                print("arquivo salvo: " + nomeArquivo + ".pdf")
                sleep(self.tempoEspera["medio"])
            else:
                print("não foi possivel salvar o Arquivo erro2")
                

    def sairLogin(self):
        self.pagina.locator("div.avatar").click()
        self.pagina.locator("a.botao.sair").click()
        self.pagina.locator("#s4-titlerow .menu-area").click()
        sleep(self.tempoEspera["rapido"])
        print("logof...")
        self.logado = False

    def fecharPagina(self):
        self.pagina.close()
    def fecharBrowser(self):
        self.browser.close
    def fecharAsyncPlay(self):
        self.asyncPlay.stop()
        self.fim = time()

    def tempoTotal(self):
        if self.fim == 0:
            return timedelta(seconds = (time() - self.inicio))
        else:
            return timedelta(seconds = (self.fim - self.inicio))

    def getMes(self,mesAno):
        mes = mesAno.split('/')
        return self.num2mes.setdefault(mes[0],'NOP')
