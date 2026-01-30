def create_stats_table(df, sample_name_column, parameters, output_path):
    df = df[[sample_name_column] + parameters]
    df_stats = df.groupby(sample_name_column).describe()  # .transpose()
    df_stats.to_excel(output_path)
