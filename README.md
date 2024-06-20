.\venv\Scripts\activate

pip install -r requirements.txt

uvicorn server:app --reload

pip install -r requirements.txt

input:

  - Thông tin order: database/df_order.csv

  - Thông tin layout warehouse: database/df_layout.csv

output:

- Mô phỏng tuyến đường di chuyển: output/output_simulation_wave.csv
  
run algorithm: python find_route.py