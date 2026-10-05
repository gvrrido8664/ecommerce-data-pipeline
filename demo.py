"""Datos inventados; demuestra cardinalidad y KPIs sin descargar Olist."""
from pathlib import Path
import pandas as pd
from scripts.pipeline import transform, kpis

ROOT = Path(__file__).resolve().parent

def demo():
    orders = pd.DataFrame([
        ['DEMO-1','C1','delivered','2026-01-01','2026-01-04','2026-01-05'],
        ['DEMO-2','C2','delivered','2026-01-01','2026-01-07','2026-01-05'],
        ['DEMO-3','C3','delivered','2026-01-01','2026-01-05 12:00','2026-01-05'],
        ['DEMO-4','C4','delivered','2026-01-01','2026-01-03','2026-01-05'],
    ],columns=['order_id','customer_id','order_status','order_purchase_timestamp','order_delivered_customer_date','order_estimated_delivery_date'])
    items = pd.DataFrame([['DEMO-1',10,2],['DEMO-1',20,3],['DEMO-2',40,5],['DEMO-3',50,5],['DEMO-4',60,6]],columns=['order_id','price','freight_value'])
    customers = pd.DataFrame([['C1','SP'],['C2','RJ'],['C3','SP'],['C4','MG']],columns=['customer_id','customer_state'])
    frame = transform(orders,items,customers)
    assert len(frame)==4 and frame.order_id.is_unique
    assert frame.loc[frame.order_id=='DEMO-1','price'].item()==30
    assert kpis(frame)['porcentaje_a_tiempo']==50
    assert frame.loc[frame.order_id=='DEMO-3','estado_entrega'].item()=='Atrasado'
    try:
        transform(pd.concat([orders,orders.iloc[:1]]),items,customers)
        raise AssertionError('Duplicate order accepted')
    except ValueError:
        pass
    invalid=items.astype({'price':float}); invalid.loc[0,'price']=float('inf')
    try:
        transform(orders,invalid,customers)
        raise AssertionError('Importe infinito aceptado')
    except ValueError:
        pass
    dest = ROOT/'demo_output'; dest.mkdir(exist_ok=True)
    frame.to_csv(dest/'pedidos_sinteticos.csv',index=False)
    import json
    (dest/'kpis.json').write_text(json.dumps(kpis(frame),ensure_ascii=False,indent=2),encoding='utf-8')
    rows = ''.join(f'<tr><td>{r.order_id}</td><td>{r.customer_state}</td><td>{r.item_count}</td><td>{r.estado_entrega}</td><td>{r.dias_diferencia:g}</td></tr>' for r in frame.itertuples())
    (dest/'reporte.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>Demo logística</title><style>body{font:18px Arial;max-width:1000px;margin:60px auto;color:#183141}h1{font-size:36px}table{border-collapse:collapse;width:100%;margin-top:40px}td,th{padding:18px;text-align:left;border-bottom:1px solid #ccd}p{line-height:1.6}</style><h1>Análisis logístico</h1><p>Demostración con datos sintéticos. No son resultados de Olist.</p><p><b>4 pedidos · 50% a tiempo · 1,25 días de retraso medio</b><br>El pedido con dos ítems se cuenta una sola vez. El retraso de medio día también se detecta.</p><table><tr><th>Pedido</th><th>Estado BR</th><th>Ítems</th><th>Entrega</th><th>Días de diferencia</th></tr>'+rows+'</table></html>',encoding='utf-8')
    print('Demo y comprobaciones correctas:',kpis(frame))

if __name__=='__main__':
    demo()
