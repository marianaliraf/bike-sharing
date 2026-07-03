import joblib
import pandas as pd


class BikeSharingPredictor:
    def __init__(self):
        """
        Inicializa o preditor de demanda de bicicletas.

        Carrega o modelo treinado e as colunas de features esperadas
        de arquivos persistidos, garantindo que os dados de inferência
        tenham a mesma estrutura que os dados de treinamento.
        """
        self.model = joblib.load('artefacts/bike_sharing_xgb_model.pkl')
        self.feature_columns = joblib.load('artefacts/feature_columns.pkl')
        print("Modelo e colunas de features carregados com sucesso de 'artefacts/'.")

    def _create_features(self, df):
        """
        Aplica a mesma engenharia de atributos usada durante o treinamento.

        Cria as variáveis 'period_day', 'is_weekend', 'is_rush_hour'
        e 'is_bad_weather' a partir das colunas existentes no DataFrame.

        Args:
            df (pd.DataFrame): DataFrame com os dados brutos de entrada.

        Returns:
            pd.DataFrame: DataFrame com as novas features criadas.
        """
        # Garante que estamos trabalhando em uma cópia para evitar SettingWithCopyWarning
        df_processed = df.copy()

        # 1. period_day (Madrugada: 0-5, Manhã: 6-11, Tarde: 12-17, Noite: 18-23)
        df_processed['period_day'] = 0 # Valor padrão
        df_processed.loc[(df_processed['hr'] >= 0) & (df_processed['hr'] <= 5), 'period_day'] = 1  # Madrugada
        df_processed.loc[(df_processed['hr'] >= 6) & (df_processed['hr'] <= 11), 'period_day'] = 2 # Manhã
        df_processed.loc[(df_processed['hr'] >= 12) & (df_processed['hr'] <= 17), 'period_day'] = 3 # Tarde
        df_processed.loc[(df_processed['hr'] >= 18) & (df_processed['hr'] <= 23), 'period_day'] = 4 # Noite

        # 2. is_weekend (0 = Não é fim de semana, 1 = É fim de semana)
        df_processed['is_weekend'] = 0
        df_processed.loc[(df_processed['weekday'] == 0) | (df_processed['weekday'] == 6), 'is_weekend'] = 1

        # 3. is_rush_hour (1 = hora de pico, 0 = não hora de pico)
        # Horários de pico: 7-9h (manhã) e 17-19h (tarde/noite)
        df_processed['is_rush_hour'] = df_processed['hr'].apply(lambda hr: 1 if (hr >= 7 and hr <= 9) or (hr >= 17 and hr <= 19) else 0)

        # 4. is_bad_weather (1 = tempo ruim, 0 = tempo bom/regular)
        # Tempo ruim: weathersit >= 3 (chuva leve/neve, chuva forte/neve)
        df_processed['is_bad_weather'] = df_processed['weathersit'].apply(lambda x: 1 if x >= 3 else 0)

        return df_processed

    def _prepare_data(self, df):
        """
        Prepara os dados para a predição, garantindo a consistência das colunas.

        Remove colunas que não são features para o modelo e garante que a ordem
        das colunas seja a mesma utilizada durante o treinamento.

        Args:
            df (pd.DataFrame): DataFrame com os dados (já com features engenheiradas).

        Returns:
            pd.DataFrame: DataFrame pronto para ser usado no modelo.

        Raises:
            ValueError: Se as colunas do DataFrame não corresponderem às colunas
                        esperadas pelo modelo.
        """
        # Verificar se todas as colunas esperadas estão presentes após a engenharia de features
        missing_cols = set(self.feature_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Colunas de features ausentes no DataFrame de entrada após engenharia: {missing_cols}")

        # Reordenar as colunas para corresponder à ordem de treinamento
        # e selecionar apenas as colunas que o modelo espera
        df_final = df[self.feature_columns]

        return df_final

    def predict(self, new_raw_data):
        """
        Realiza a predição de demanda de bicicletas em novos dados brutos.

        Aplica a engenharia de atributos, prepara os dados e utiliza o modelo
        carregado para fazer as previsões.

        Args:
            new_raw_data (pd.DataFrame): Novos dados de entrada brutos para predição.
                                         Deve conter as colunas necessárias para
                                         a engenharia de atributos ('hr', 'weekday', 'weathersit')
                                         e as demais features esperadas pelo modelo.

        Returns:
            np.ndarray: Array contendo as previsões de demanda.
        """
        # 1. Engenharia de atributos
        print("Aplicando engenharia de atributos...")
        data_with_features = self._create_features(new_raw_data.copy())

        # 2. Preparação dos dados
        print("Preparando dados para o modelo...")
        prepared_data = self._prepare_data(data_with_features)

        # 3. Predição
        print("Realizando predições...")
        predictions = self.model.predict(prepared_data)

        return predictions