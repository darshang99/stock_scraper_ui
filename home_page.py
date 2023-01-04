import streamlit as st
import webbrowser
from stocksymbol import StockSymbol
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import yfinance as yf
import plotly.express as px
from mpl_finance import candlestick_ohlc
import requests
import json
from streamlit_lottie import st_lottie
# Clears the contents of the sidebar

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=['Home','Stock-Details','Contact'],
        icons=["house","graph-up","phone"],
        menu_icon= "cast",
        default_index=0,
    )
def load_lottiefile(url:str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        else:
            return r.json()
if selected =="Home":
    st.title("Stock Price Scraper")
    st.empty()
    lottie_stock = load_lottiefile("https://assets6.lottiefiles.com/packages/lf20_wh4gk3bb.json")
    st_lottie(
        lottie_stock,key="stock",width=300 
        #this is for the ones that are downloaded speed =1,
        # reverse = False,
        # loop  = True,
        # quality = "high",
        # key=None,
        # height = None,
        # width = None,
        )
    st.sidebar.success("Select the stock here!")

    api_key = 'ee43e699-2411-4e23-9491-a617bb1f1239'
    ss = StockSymbol(api_key)

    symbol_list_ind = ss.get_symbol_list(market="India")
    # Get cryptocurrency data
    stocksDict = {}

    for stock in symbol_list_ind:
        key = stock.get('longName')
        value = stock.get('symbol')
        stocksDict[key] = value

    st.subheader("Select a stock You want update on!")
    selected_stock = st.selectbox("Select a stock",stocksDict.keys())

    if "stock_name" not in st.session_state:
        st.session_state["stock_name"] = ""
        st.session_state["stock_symbol"] = ""

    st.markdown('''<br>''',unsafe_allow_html=True)
    graphs = ['Line Graph','Candle-Stick','Bar chart','Scatter plot']
    graph_type = st.selectbox('Select a type of the graph',graphs)

    if "graph_type" not in st.session_state:
        st.session_state["graph_type"] = ""

    submit = st.button("Submit")

    if submit:
        st.session_state["stock_name"] = selected_stock
        st.session_state["stock_symbol"] = stocksDict[selected_stock]
        st.session_state["graph_type"] = graph_type
        st.markdown('''<br>''',unsafe_allow_html=True)
        st.subheader("Move to the stock details page to find the recent updates about ",selected_stock)

elif selected == "Stock-Details":
    st.sidebar.header="stock_details"
    def draw_scatter(stock_name,stock_symbol):
        ticker = yf.Ticker(stock_symbol)
        hist = ticker.history(period="1y")
        fig = go.Figure()
        # Add a scatter trace
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], marker=dict(size=10, color='red')))
        fig.update_layout(
            title=stock_name+ 'Stock Price',
            xaxis_title='Date',
            yaxis_title='Price (INR)',
            height = 550,
            font=dict(family='Courier New, monospace', size=12, color='#7f7f7f'))

        # Show the plot
        st.plotly_chart(fig)

    def draw_candleStick(stock_name,stock_symbol):
        ticker = yf.Ticker(stock_symbol)
        hist = ticker.history(period="1y")

        # Prepare the data for the candlestick chart
        data = [go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'])]

        # Create the figure
        fig = go.Figure(data=data)

        # Specify the layout
        fig.update_layout(
            title=stock_name+ 'Stock Price',
            xaxis_title='Date',
            yaxis_title='Price (INR)',
            height = 550,
            width = 700,
            font=dict(family='Courier New, monospace', size=12, color='#7f7f7f'))

        # Show the plot
        # Add the figure to the app
        st.plotly_chart(fig)

    def draw_bar(stock_name,stock_symbol):
        ticker = yf.Ticker(stock_symbol)
        hist = ticker.history(period="1y")
        st.bar_chart(hist['Close'],height=550)
        st.title(stock_name," price details")
        # Create the bar graph

    def draw_line(stock_name,stock_symbol):    
        ticker = yf.Ticker(stock_symbol)
        hist = ticker.history(period="1y")
        st.line_chart(hist['Close'],height=550)


    stock_name = st.session_state["stock_name"]
    stock_symbol = st.session_state["stock_symbol"]
    graph_type = st.session_state["graph_type"]
    st.title("{} stock updates are here".format(stock_name))

    if graph_type =="Candle-Stick":
        draw_candleStick(stock_name,stock_symbol)

    elif graph_type == "Scatter plot":
        draw_scatter(stock_name,stock_symbol)

    elif graph_type == "Bar chart":
        draw_bar(stock_name,stock_symbol)
    elif graph_type =="Line Graph":
        draw_line(stock_name,stock_symbol)

elif selected == "Contact":
    st.header(":mailbox: Get in touch with me!")
    st.markdown('''<br>''',unsafe_allow_html=True)
    st.subheader("About me")
    st.write("Im Darshan Laxman Gouda pursuing my Computer science and engineering degree from St. Joseph Engineering College")
    st.write("Im very creative and I have good leadership skills and also I love to explore more things and Im open to new technologies.")
    st.markdown("You can find me on:")

    st.markdown(
            """
            <img src="linkedin_icon.png" width="30">
            <a href="https://www.linkedin.com/in/your_handle/">LinkedIn</a>
            """
        , unsafe_allow_html=True)
    st.markdown(
            """
            <img src="GitHub-Mark.png" width="40">
            <a href="https://github.com/your_handle">GitHub</a>
            """
        , unsafe_allow_html=True)

    lottie_hello = load_lottiefile("https://assets8.lottiefiles.com/packages/lf20_calza6zj.json")
    st_lottie(
        lottie_hello,key="hello",width=300 
        #this is for the ones that are downloaded speed =1,
        # reverse = False,
        # loop  = True,
        # quality = "high",
        # key=None,
        # height = None,
        # width = None,
        )
    contactform = """
    <form action = "https://formsubmit.co/darshangouda518@gmail.com" method = "POST">
        <input type="hidden" name="_captcha" value = "false">
        <input type = "text" name= "name" placeholder="Your name" required>
        <input type = "email" name= "email" placeholder="Your email" required>
        <textarea name = "message" placeholder="Details of your problem"></textarea>
        <button type = "submit"> Send </button>
    """
    st.markdown(contactform, unsafe_allow_html=True)

    def local_css(filename):
        with open(filename) as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)



    local_css("style/style.css")

    st.markdown('''<br>''',unsafe_allow_html=True)

