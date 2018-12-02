from atlas_auto import at

test_list = (29004,
             10001,
             39001,
             36001,
             13001,
             36002,
             38001,
             40001,
             43001,
             39002,
             10002,
             45001)

atlas = at(
    data_uri='./data/profile_data_structure.xlsx',
    wards_uri='./hrrp_shapes/wards/merge.shp',
    palika_uri='./hrrp_shapes/palika/GaPaNaPa_hrrp.shp',
    dists_uri='./hrrp_shapes/districts/Districts_hrrp.shp',
    dists_syle='./styles/dist_style.qml',
    pka_style='./styles/palika_style.qml',
    pka_hide_style='./styles/palika_hide_style.qml',
    ward_style='./styles/ward_style.qml',
    parent_join_cd='N_WCode',
    to_join_code='ward',
    pka_list=test_list)

atlas.make_maps()
