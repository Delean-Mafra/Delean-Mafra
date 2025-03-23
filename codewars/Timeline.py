from datetime import datetime, timedelta
# By Delean Mafra
def get_date(start, end, width, pos):
    # Calcula a diferença total de tempo em segundos
    total_time_diff = (end - start).total_seconds()
    
    # Calcula a proporção da posição no gráfico
    proportion = pos / width
    
    # Calcula o número de segundos para adicionar ao start
    seconds_to_add = total_time_diff * proportion
    
    # Adiciona os segundos calculados ao datetime inicial
    result_date = start + timedelta(seconds=seconds_to_add)
    
    # Formata o resultado no formato ISO sem os segundos
    return result_date.strftime("%Y-%m-%dT%H:%M")


import datetime

def get_date(start: datetime.datetime, end: datetime.datetime, width: int, pos: int) -> str:
    """
    Calculates the date and time on a timeline corresponding to a given position.

    Args:
        start: datetime.datetime object representing the start date of the timeline.
        end: datetime.datetime object representing the end date of the timeline.
        width: integer representing the width of the graph in pixels.
        pos: integer representing the position of the red line in pixels.

    Returns:
        An ISO formatted string representing the date and time at the given position,
        with seconds stripped (e.g., "2007-05-25T14:24").
    """
    duration = end - start
    proportion = pos / width
    time_difference = duration * proportion
    result_date = start + time_difference
    return result_date.isoformat(timespec='minutes')
