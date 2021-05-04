import data_wrangling_poll, data_wrangling_traffic

start_date = '2021-04-01'
end_date = '2021-04-30'

data_wrangling_traffic.wrangle_it()
data_wrangling_poll.wrangle_it()

import charts_BR, latex_BR

charts_BR.make_plots(start_date, end_date)
latex_BR.make_latex(start_date, end_date)

