from smolagents import DuckDuckGoSearchTool,tool
import yfinance as yf
import datetime
import pytz
import os
import platform
import time

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def math_operation(arg1: float, arg2: float, operation: str) -> float:
    """A tool that performs basic arithmetic operations.
    
    Args:
        arg1: The first number.
        arg2: The second number.
        operation: The operation to perform ('add', 'subtract', 'multiply', 'divide').
    
    Returns:
        The result of the operation.
    """
    match operation:
        case "add":
            return arg1 + arg2
        case "subtract":
            return arg1 - arg2
        case "multiply":
            return arg1 * arg2
        case "divide":
            return arg1 / arg2 if arg2 != 0 else float("inf")  # Evita divisão por zero
        case _:
            raise ValueError("Invalid operation. Use 'add', 'subtract', 'multiply', or 'divide'.")

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"

@tool
def internet_search(query: str) -> str:
    """
    A tool to search the internet using DuckDuckGo.
    
    Args:
        query: The search query.
    
    Returns:
        The top search result.
    """
    seach = DuckDuckGoSearchTool()
    results = seach.forward(query)
    return results if results else "No results found."


@tool
def get_stock_info(ticker: str) -> str:
    """
    Fetches general information about a given stock.
    Args:
        ticker: The stock symbol (e.g., "AAPL" for Apple, "MSFT" for Microsoft).
    
    Returns:
        A summary of the stock information.
    """
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return (f"Company: {info.get('longName', 'N/A')}\n"
                f"Sector: {info.get('sector', 'N/A')}\n"
                f"Industry: {info.get('industry', 'N/A')}\n"
                f"Country: {info.get('country', 'N/A')}\n"
                f"Market Cap: {info.get('marketCap', 'N/A')}\n"
                f"PE Ratio: {info.get('trailingPE', 'N/A')}")
    except Exception as e:
        return f"Error fetching stock information: {str(e)}"

@tool
def get_stock_price(ticker: str) -> str:
    """
    Fetches the current stock price.
    Args:
        ticker: The stock symbol (e.g., "AAPL", "MSFT").
    
    Returns:
        The latest stock price.
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return f"The latest closing price for {ticker} is ${price:.2f}."
    except Exception as e:
        return f"Error fetching stock price: {str(e)}"

@tool
def compare_stocks(ticker1: str, ticker2: str, period: str = "1y") -> str:
    """
    Compares the performance of two stocks over a given period.
    Args:
        ticker1: The first stock symbol.
        ticker2: The second stock symbol.
        period: The time period for comparison (e.g., "1mo", "6mo", "1y").
    
    Returns:
        A summary of their percentage change over the period.
    """
    try:
        stock1 = yf.Ticker(ticker1).history(period=period)["Close"]
        stock2 = yf.Ticker(ticker2).history(period=period)["Close"]

        if stock1.empty or stock2.empty:
            return "Insufficient data for comparison."

        change1 = ((stock1.iloc[-1] - stock1.iloc[0]) / stock1.iloc[0]) * 100
        change2 = ((stock2.iloc[-1] - stock2.iloc[0]) / stock2.iloc[0]) * 100

        return (f"{ticker1}: {change1:.2f}% over {period}\n"
                f"{ticker2}: {change2:.2f}% over {period}")
    except Exception as e:
        return f"Error comparing stocks: {str(e)}"

@tool
def get_index_price(index: str) -> str:
    """
    Fetches the current price of a stock market index.
    Args:
        index: The index ticker (e.g., "^GSPC" for S&P 500, "^DJI" for Dow Jones, "^IXIC" for Nasdaq).
    
    Returns:
        The latest closing price of the index.
    """
    try:
        ticker = yf.Ticker(index)
        price = ticker.history(period="1d")["Close"].iloc[-1]
        return f"The latest closing price for {index} is {price:.2f}."
    except Exception as e:
        return f"Error fetching index price: {str(e)}"

@tool
def get_interest_rates() -> str:
    """
    Fetches the latest Selic, CDI, and IPCA rates.
    Returns:
        The latest values for Brazil's key interest rates.
    """
    import requests
    try:
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json")  # SELIC
        selic = response.json()[0]['valor']

        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json")  # CDI
        cdi = response.json()[0]['valor']

        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json")  # IPCA
        ipca = response.json()[0]['valor']

        return (f"Selic atual: {selic}% ao ano\n"
                f"CDI atual: {cdi}% ao ano\n"
                f"IPCA acumulado: {ipca}%")
    except Exception as e:
        return f"Erro ao buscar taxas de juros: {str(e)}"


@tool
def compare_fixed_income(amount: float, period: int, cdi_percentage: float) -> str:
    """
    Compares the return of a CDB vs. savings over a given period.
    Args:
        amount: The initial investment amount.
        period: The investment duration in months.
        cdi_percentage: The CDB return as a percentage of the CDI.
    
    Returns:
        The final amount in CDB vs. savings.
    """
    import requests
    try:
        # Buscar CDI atual
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json")
        cdi = float(response.json()[0]['valor']) / 100

        # Poupança rende 70% da Selic quando Selic > 8.5%
        response = requests.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json")
        selic = float(response.json()[0]['valor']) / 100
        poupanca_rendimento = 0.7 * selic if selic > 0.085 else 0.005

        # Calcular rendimentos
        cdb_final = amount * ((1 + (cdi * cdi_percentage / 100)) ** (period / 12))
        poupanca_final = amount * ((1 + poupanca_rendimento) ** (period / 12))

        return (f"Após {period} meses:\n"
                f"CDB ({cdi_percentage}% do CDI): R$ {cdb_final:.2f}\n"
                f"Poupança: R$ {poupanca_final:.2f}")
    except Exception as e:
        return f"Erro ao calcular rendimentos: {str(e)}"
    
@tool
def shutdown_computer(delay: str = "0") -> str:
    """
    Uma tool que desliga o computador após um delay opcional.
    
    Args:
        delay: Uma string que representa o tempo de espera antes do desligamento 
               (exemplos: "1 min", "30 sec", "1 hr"). O valor padrão "0" desliga imediatamente.
    
    Returns:
        Uma mensagem indicando que o comando de desligamento foi enviado.
    """


    try:
        delay = delay.strip()
        if delay in ["", "0"]:
            seconds = 0
        else:
            parts = delay.split()
            if len(parts) != 2:
                return "Formato de delay inválido. Use '1 min', '30 sec' ou '1 hr'."
            value = float(parts[0])
            unit = parts[1].lower()
            if unit.startswith("sec"):
                seconds = value
            elif unit.startswith("min"):
                seconds = value * 60
            elif unit.startswith("hr"):
                seconds = value * 3600
            else:
                return "Unidade de tempo inválida. Use 'sec', 'min' ou 'hr'."
    except Exception as e:
        return f"Erro ao interpretar o delay: {str(e)}"
    
    # Aguarda o tempo especificado, se houver
    if seconds > 0:
        time.sleep(seconds)
    
    # Determina o sistema operacional e emite o comando de desligamento
    current_os = platform.system()
    if current_os == "Windows":
        os.system("shutdown /s /t 0")
    elif current_os in ["Linux", "Darwin"]:
        os.system("sudo shutdown -h now")
    else:
        return f"Sistema operacional {current_os} não suportado para desligamento automático."
    
    return "Comando de desligamento enviado."
