 from app import app, db                                                                                                                                          
                                                                                                                                                                  
 def test_db_connection():                                                                                                                                        
     try:                                                                                                                                                         
         with app.app_context():                                                                                                                                  
             db.engine.connect()                                                                                                                                  
         print("Database connection successful!")                                                                                                                 
     except Exception as e:                                                                                                                                       
         print(f"Database connection failed. Error: {e}")                                                                                                         
                                                                                                                                                                  
 if __name__ == '__main__':                                                                                                                                       
     test_db_connection()                                                                                                                                         
     app.run(host='0.0.0.0', port=5000, debug=True)  