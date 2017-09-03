"""Note that dash_parser requires Dash's default Skeleton CSS system."""

# Import required libraries
import six
import dash_html_components as html


# Conversions
COLUMNS = {
    '1': 'one columns',
    '2': 'two columns',
    '3': 'three columns',
    '4': 'four columns',
    '5': 'five columns',
    '6': 'six columns',
    '7': 'seven columns',
    '8': 'eight columns',
    '9': 'nine columns',
    '10': 'ten columns',
    '11': 'eleven columns',
    '12': 'twelve columns'}

OFFSETS = {
    '1': 'offset-by-one',
    '2': 'offset-by-two',
    '3': 'offset-by-three',
    '4': 'offset-by-four',
    '5': 'offset-by-five',
    '6': 'offset-by-six',
    '7': 'offset-by-seven',
    '8': 'offset-by-eight',
    '9': 'offset-by-nine',
    '10': 'offset-by-ten',
    '11': 'offset-by-eleven',
    '12': 'offset-by-twelve'}


# Functions
def parse_columns(format_string):
    """Parse quickhand skeleton notation into valid Skeleton CSS classes

    Use 'x' or ',' to separate column and row length, and use 'o' to specify
    offsets when needed.

    Example
    -------
        '10o2 x 2' : 'ten-columns offset-by-two'
        '10o2' : 'ten-columns offset-by-two'
        '3 x 2' : 'three-columns'

    """
    offset = None

    if 'x' in format_string:
        string = format_string.split('x')[0].strip()
    elif ',' in format_string:
        string = format_string.split(',')[0].strip()
    else:
        raise Exception('Cannot parse formatting string {}.'.format(format_string))

    if 'o' in string:
        s = string.split('o')
        string = s[0].strip()
        offset = s[1].strip()

    final_string = COLUMNS[string]

    if offset is not None:
        final_offset = OFFSETS[offset]
        final_string = final_string + ' ' + final_offset

    return final_string


def create_grid_layout(format_list):
    """Make Dash HTML layout from a format list.

    Note: Non-recursive implementation since Skeleton does not treat rows and columns
    as the same thing. Recursive implentation fails at 3rd call.

    """
    row_list = []
    for row in format_list:

        column_list = []
        for column in row:

            if type(column) is not list:
                column_div = html.Div([html.P('FILLER_TEXT \n FILLER_TEXT \n FILLER_TEXT \n FILLER_TEXT')], className=parse_columns(column))
                column_list.append(column_div)

            else:
                sub_row_list = []
                for sub_row in column:

                    sub_row_div = html.Div([html.P('FILLER_TEXT \n FILLER_TEXT \n FILLER_TEXT \n FILLER_TEXT')])
                    sub_row_list.append(sub_row_div)

                column_div = html.Div(sub_row_list, className=parse_columns(column[0]))
                column_list.append(column_div)

        row_div = html.Div(column_list, className='row')
        row_list.append(row_div)

    return row_list
