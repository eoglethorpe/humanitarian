from atlas_auto import at

test_list = (24001,
                24002,
                24003,
                24004,
                24005,
                24006,
                24007,
                24008,
                24009,
                24010,
                24011,
                24012,
                24013)

atlas = at(
    data_uri='./data/profile_data_structure_template.xlsx',
    wards_uri='./hrrp_shapes/wards/merge.shp',
    palika_uri='./hrrp_shapes/palika/GaPaNaPa_hrrp.shp',
    dists_uri='./hrrp_shapes/districts/Districts_hrrp.shp',
    dists_syle='./styles/dist_style.qml',
    pka_style='./styles/palika_style.qml',
    pka_hide_style='./styles/palika_hide_style.qml',
    ward_style='./styles/ward_style.qml',
    parent_join_cd='N_WCode',
    to_join_code='ward',
    pka_list=test_list,
    img_type = 'img')

atlas.make_maps()
