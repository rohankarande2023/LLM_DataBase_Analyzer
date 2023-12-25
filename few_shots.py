few_shots=[
    {
        'Question':"How many orange colored t-shirts do we have of Polo in size small?",
        'SQLQuery':"select sum(stock_quantity) from t_shirts WHERE brand = 'Polo' and color='Orange' and size='S'",
        'SQLResult':"Result of the SQL query",
        'Answer': "25"
    },
     {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': "22292"},
    
      {'Question': "If we have to sell all the Polo T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """select SUM(t.total_amount-(t.total_amount*d.pct_discount/100)) as total_revenue from (SELECT SUM(price*stock_quantity) as total_amount, t_shirt_id FROM t_shirts WHERE brand = 'Polo' group by t_shirt_id)as t left join discounts as d on t.t_shirt_id=d.t_shirt_id """,
     'SQLResult': "Result of the SQL query",
     'Answer': "311487.5"},
    
      {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levis'",
      'SQLResult': "Result of the SQL query",
      'Answer' : "317200"},
    
     {'Question': "If we have to sell all Yellow Boss T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """select SUM(t.total_amount-(t.total_amount*d.pct_discount/100)) as total_revenue from (SELECT SUM(price*stock_quantity) as total_amount, t_shirt_id FROM t_shirts WHERE brand = 'Boss' and color='Yellow' group by t_shirt_id)as t left join discounts as d on t.t_shirt_id=d.t_shirt_id """,
     'SQLResult': "Result of the SQL query",
     'Answer': "248760.0"},
     {'Question': "How many Orange color Polo shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Polo' AND color = 'Orange'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "100"
     },
      {'Question': "Which brand offers the maximum discount?",
     'SQLQuery' : "select top 1 brand, max(pct_discount) as max_discount from discounts d inner join t_shirts t on t.t_shirt_id=d.t_shirt_id group by brand order by max_discount desc",
     'SQLResult': "Result of the SQL query",
     'Answer' : "Levis"
     }

    
]