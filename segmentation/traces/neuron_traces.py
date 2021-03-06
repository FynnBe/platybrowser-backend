#! /g/arendt/EM_6dpf_segmentation/platy-browser-data/software/conda/miniconda3/envs/platybrowser/bin/python
import json
import numpy as np
import pandas as pd
from mmpb.export import extract_neuron_traces_from_nmx, traces_to_volume, make_traces_table


def get_resolution(scale, use_nm=True):
    if use_nm:
        res0 = [25, 10, 10]
        res1 = [25, 20, 20]
    else:
        res0 = [0.025, 0.01, 0.01]
        res1 = [0.025, 0.02, 0.02]
    resolutions = [res0] + [[re * (2 ** (i)) for re in res1] for i in range(5)]
    return np.array(resolutions[scale])


def export_traces():
    folder = '/g/kreshuk/data/arendt/platyneris_v1/tracings/kevin'
    ref_path = '../../data/rawdata/sbem-6dpf-1-whole-raw.n5'
    seg_out_path = './sbem-6dpf-1-whole-traces.n5'
    table_out_path = './default.csv'

    ref_scale = 3
    cell_seg_info = {'path': '../../data/0.6.5/images/local/sbem-6dpf-1-whole-segmented-cells.n5',
                     'scale': 2}
    nucleus_seg_info = {'path': '../../data/0.0.0/images/local/sbem-6dpf-1-whole-segmented-nuclei.n5',
                        'scale': 0}

    print("Extracting traces ...")
    traces = extract_neuron_traces_from_nmx(folder)
    print("Found", len(traces), "traces")

    resolution = get_resolution(ref_scale)
    n_scales = 4
    scale_factors = n_scales * [[2, 2, 2]]
    print("Write trace volume ...")
    traces_to_volume(traces, ref_path, ref_scale, seg_out_path, resolution, scale_factors)

    print("Make table for traces ...")
    make_traces_table(traces, ref_scale, resolution, table_out_path,
                      cell_seg_info, nucleus_seg_info)


def get_cell_ids():
    table_path = './sbem-6dpf-1-whole-traces-table-default.csv'
    table = pd.read_csv(table_path, sep='\t')
    cell_ids = table['cell_id'].values
    cell_ids = cell_ids[cell_ids != 0].tolist()
    with open('./trace_cell_ids.json', 'w') as f:
        json.dump(cell_ids, f)


# for debugging
def check_extraction():
    import elf.skeleton.io as skio
    path = '/g/kreshuk/data/arendt/platyneris_v1/tracings/kevin/knm_ApNS_6dpf_neuron_traces.4138.nmx'
    # path = '/g/kreshuk/data/arendt/platyneris_v1/tracings/comm_sec_seg.019.nmx'
    skel = skio.read_nml(path)
    search_str = 'neuron_id'
    for k, v in skel.items():
        sub = k.find(search_str)
        beg = sub + len(search_str)
        end = k.find('.', beg)
        n_id = int(k[beg:end])

        if n_id != 10:
            continue

        print(k)
        print(n_id)
        print(v)


if __name__ == '__main__':
    export_traces()
    # get_cell_ids()
    # check_extraction()
