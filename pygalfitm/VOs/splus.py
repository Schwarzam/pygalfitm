def get_sersic_splus(ra, dec):
    
    lb_a : str = ""
    leffective_r : str = ""
    lpa : str = ""
    lmagnitude : str = ""

    for band in ['R', 'I', 'G']:
        band = band.lower()

        table = conn.query(f"""
            select * from "idr4_single"."idr4_single_{band}" as x
            where 
            1 = CONTAINS( POINT('ICRS', x.ra_{band}, x.dec_{band}), 
            CIRCLE('ICRS', {ra}, {dec}, 0.0015))
        """)
        
        lb_a += "," + str( table[0][f"B_{band}"]/table[0][f"A_{band}"] )
        leffective_r += "," + str( table[0][f"FLUX_RADIUS_50_{band}"] )
        lpa += "," + str( table[0][f"THETA_{band}"] )
        lmagnitude += "," + str( table[0][f"{band}_auto"]  )

    lb_a = lb_a[1:]
    leffective_r = leffective_r[1:]
    lpa = lpa[1:]
    lmagnitude = lmagnitude[1:]

    return lb_a, leffective_r, lpa, lmagnitude