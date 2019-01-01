import os
import utils
import pandas as pd
import itertools
from multiprocessing.dummy import Pool as ThreadPool
import time

field_names = ['index', 'volume', 'surface_area', 'filename', 'dose', 'area', 'time', 'vol/sa']
start = time.time()
new_file_path = '/Users/travisclarke/Documents/Masters/MaFIA EtOH Images/New Mafia'
old_file_path = '/Users/travisclarke/Documents/Masters/MaFIA EtOH Images/Old Mafia'
new_tifs = [os.path.join(new_file_path, path) for path in os.listdir(new_file_path) if ('.tif' in path)]
old_tifs = [os.path.join(old_file_path, path) for path in os.listdir(old_file_path) if ('.tif' in path)]
microglia_dicts_old = []
microglia_dicts_new = []

pool = ThreadPool(8)
pool.imap_unordered(utils.process_img, zip(old_tifs, itertools.repeat(microglia_dicts_old)))
pool.close()
pool.join()

pool = ThreadPool(8)
pool.imap_unordered(utils.process_img, zip(new_tifs, itertools.repeat(microglia_dicts_new)))
pool.close()
pool.join()

end = time.time()
print(f'it took this long {end-start}')

old_data = pd.DataFrame(microglia_dicts_old)
new_data = pd.DataFrame(microglia_dicts_new)
writer_new = pd.ExcelWriter(os.path.join(new_file_path,'results.xlsx'))
writer_old = pd.ExcelWriter(os.path.join(old_file_path,'results.xlsx'))
old_data.to_excel(writer_old, 'Old Mafia')
new_data.to_excel(writer_new, 'New Mafia')
writer_old.save()
writer_new.save()


# VTA_1g_quarter = data[(data.dose == '1g') & (data.area == 'VTA') & (data.time == '0.25')]
# VTA_1g_half = data[(data.dose == '1g') & (data.area == 'VTA') & (data.time == '0.5')]
# VTA_1g_one = data[(data.dose == '1g') & (data.area == 'VTA') & (data.time == '1')]
# VTA_1g_two = data[(data.dose == '1g') & (data.area == 'VTA') & (data.time == '2')]
# VTA_2g = data[(data.dose == '2g') & (data.area == 'VTA')]
# VTA_4g = data[(data.dose == '4g') & (data.area == 'VTA')]
# VTA_Sal = data[(data.dose == 'Sal') & (data.area == 'VTA')]
# NAc_1g = data[(data.dose == '1g') & (data.area == 'NAc')]
# NAc_2g = data[(data.dose == '2g') & (data.area == 'NAc')]
# NAc_4g = data[(data.dose == '4g') & (data.area == 'NAc')]
# NAc_Sal = data[(data.dose == 'Sal') & (data.area == 'NAc')]
# F, p = stats.f_oneway(VTA_1g_quarter['vol/sa'],
#                       # VTA_1g_half['vol/sa'],
#                       VTA_1g_one['vol/sa'],
#                       VTA_1g_two['vol/sa'])
# print(p)

