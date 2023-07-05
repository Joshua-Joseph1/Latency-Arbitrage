//+------------------------------------------------------------------+
//|                                                    FX_Bot_01.mq5 |
//|                                  Copyright 2022, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2022, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
double bid_offset = 0.0;
double ask_offset = 0.0;
int count =100;
int OnInit()
  {
//--- create timer
   EventSetMillisecondTimer(1);
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
      
     //File handling logic
     string text = "";
     
     int fileHandle = FileOpen("DWX\\enq_Market_Data.txt",FILE_READ|FILE_ANSI|FILE_COMMON|FILE_TXT);
     if(fileHandle!=INVALID_HANDLE){
           text = FileReadString(fileHandle);
           FileClose(fileHandle);
           //Extract rithmic quotes
           string sep=",";
           ushort u_sep;
           string result[3];
           u_sep=StringGetCharacter(sep,0);
           int k=StringSplit(text,u_sep,result);
           //Retrieve latest tick
           MqlTick lastTick;
           SymbolInfoTick(Symbol(), lastTick);
           double spread = MathAbs(NormalizeDouble(lastTick.ask-lastTick.bid, 2));
           //Print(text);
           
           double fast_bid_price = NormalizeDouble((NormalizeDouble(result[1], 5)), 5);
           double fast_ask_price = NormalizeDouble((NormalizeDouble(result[2], 5)), 5);
           //Print(fast_price-lastTick.bid);
           
           double rithmic_bid = NormalizeDouble((NormalizeDouble(result[1], 2)-bid_offset), 2);
           double rithmic_ask = NormalizeDouble((NormalizeDouble(result[2], 2)-ask_offset), 2);
           long rithmic_time = result[0];
           
           if (count == 100){
            bid_offset = MathAbs(fast_bid_price-lastTick.bid);
            ask_offset = MathAbs(fast_ask_price-lastTick.ask);
               count=0;
           }
           

           DrawQuotes(rithmic_bid,rithmic_ask);

           if (rithmic_time>lastTick.time_msc &&(rithmic_bid)>(lastTick.ask+spread)&&PositionsTotal()==0){
               Print("Rithmic faster time B "+ rithmic_bid+" "+ rithmic_ask+ "  "+lastTick.bid + " "+lastTick.ask );
               MqlTradeRequest request={};
               MqlTradeResult  result={};
               request.action   =TRADE_ACTION_DEAL;                     
               request.symbol   =Symbol();                              
               request.volume   =3.0;                                
               request.type     =ORDER_TYPE_BUY;                                  
               request.price    =SymbolInfoDouble(Symbol(),SYMBOL_ASK);
               request.sl = NormalizeDouble(SymbolInfoDouble(Symbol(),SYMBOL_BID)-(5.0),2);
               request.tp= rithmic_bid+4.5;                               
               request.deviation=0;                                  
               request.magic    =234000; 
               request.type_filling = ORDER_FILLING_IOC;                         
               OrderSend(request,result);
           }
           else if(rithmic_time>lastTick.time_msc &&(lastTick.bid-spread)>rithmic_ask&&PositionsTotal()==0){
               Print("Rithmic faster time S "+ rithmic_bid+" "+ rithmic_ask+ "  "+lastTick.bid + " "+lastTick.ask);
               MqlTradeRequest request={};
               MqlTradeResult  result={};
               request.action   =TRADE_ACTION_DEAL;                     
               request.symbol   =Symbol();                              
               request.volume   =3.0;                                
               request.type     =ORDER_TYPE_SELL;                                  
               request.price    =SymbolInfoDouble(Symbol(),SYMBOL_BID);
               request.sl = NormalizeDouble(SymbolInfoDouble(Symbol(),SYMBOL_ASK)+(5.0),2);
               request.tp= rithmic_ask-4.5;                               
               request.deviation=0;                                  
               request.magic    =234000; 
               request.type_filling = ORDER_FILLING_IOC; 
               OrderSend(request,result);  
           }
           count+=1;

     }
     
     
     

  }
//+------------------------------------------------------------------+
void DrawQuotes(double fast_bid, double fast_ask){

   ObjectDelete(_Symbol, "Bid");
   ObjectDelete(_Symbol, "Ask");
   
   ObjectCreate(_Symbol, "Bid", OBJ_HLINE,0, TimeCurrent(),fast_bid);
   ObjectSetInteger(0, "Bid", OBJPROP_COLOR,clrDarkSlateBlue);
   

   ObjectCreate(_Symbol, "Ask", OBJ_HLINE,0, TimeCurrent(),fast_ask);
   ObjectSetInteger(0, "Ask", OBJPROP_COLOR,clrDarkOrange);

}