import pandas as pd
import json
#import tkinter as tk
#from tkinter import filedialog
from flask import Flask, request, redirect, url_for, render_template
import csv 
    
app = Flask(__name__)

def generar_tabla(i_pct, n_max, modo):
    i = i_pct / 100
    
    #depende si queremos solo la fila o hasta un numero de n
    
    periodos = range(1, n_max + 1) if modo == 'hasta' else [n_max]
    data = []
    for n in periodos:
        fp = (1 + i)**n 
        pf = 1 / fp
        fa = ((1 + i)**n - 1) / i if i > 0 else n
        af = 1 / fa if fa > 0 else 0
        pa = ((1 + i)**n - 1) / (i * (1 + i)**n) if i > 0 else n
        ap = 1 / pa if pa > 0 else 0
        # Factores de Gradiente
        pg = (1/i) * (pa - (n / (1+i)**n)) if i > 0 else 0
        ag = pg / pa if pa > 0 else 0
        
        data.append([n, fp, pf, af, ap, fa, pa, ag, pg])
    
    df = pd.DataFrame(data, columns=['n', 'F/P', 'P/F', 'A/F', 'A/P', 'F/A', 'P/A', 'A/G', 'P/G'])
    return df.round(5).to_dict(orient='records')

#esta era la idea original jeje
#def guadar_json(df, intereses):
#    root = tk.Tk()
#    root.withdraw()
#    root.attributes('-topmost', True) #Nos pone la ventana de dialogo al frente
#    
#    #ahora configuramos el explorador de archivos
#    file_path = filedialog.asksaveasfilename(defaultextension=".json", 
#                                             filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
#                                            initialfile=f"tabla_factores_{intereses}%.json",
#                                            title="Guardar tabla de factores")
#    if file_path:
#        df.to_json(file_path, orient='records', indent=4)
#        print(f"Tabla de factores guardada en: {file_path}")
#    else:
#        print("Guardado cancelado.")
#        
#    root.destroy()
#    
#def guadar_csv(df, intereses):
#    root = tk.Tk()
#    root.withdraw()
#    root.attributes('-topmost', True) #Nos pone la ventana de dialogo al frente
#    
#    #ahora configuramos el explorador de archivos
#    file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
#                                             filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
#                                            initialfile=f"tabla_factores_{intereses}%.csv",
#                                            title="Guardar tabla de factores")
#    if file_path:
#        df.to_csv(file_path, index=False)
#        print(f"Tabla de factores guardada en: {file_path}")
#    else:
#        print("Guardado cancelado.")
#        
#    root.destroy()
#    
#
#interes = float(input("Ingrese la tasa de interés (en %): "))
#n_max = int(input("Ingrese el número máximo de períodos: "))
#tipo_guardado = input("¿Desea guardar la tabla en formato JSON o CSV? (Ingrese 'JSON' o 'CSV'): ").strip().upper()
#
#tabla = generar_tabla(interes, n_max)
#
#if tipo_guardado == "JSON" or tipo_guardado == "json":
#    guadar_json(tabla, interes)
#elif tipo_guardado == "CSV" or tipo_guardado == "csv":
#    guadar_csv(tabla, interes)
#else:
#    print("Formato no válido. No se guardó la tabla.")#

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    interes = float(request.form['interes'])
    n_max = int(request.form['n_max'])
    modo = request.form['modo']
    
    datos_tabla = generar_tabla(interes, n_max, modo)
    return render_template('tabla.html', datos=datos_tabla, interes=interes)

if __name__ == '__main__':
    app.run(debug=True)