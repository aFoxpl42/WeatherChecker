# TODO Choice between temp and wind on da graph
# TODO Choice between daily, and x days 
# TODO Restrucurization of the get_forecast_and_plot function
# TODO Probably can also wrap main container etc into functions to clean up the code
# TODO Will figure out later


from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from weather import get_weather_forecast, get_current_state, get_cities

cities_autocompletion = get_cities()

# UI elements
ui_container = ui.column().classes("w-full items-center gap-4")
with ui_container:
    search_word = ui.input('Enter Location', autocomplete=cities_autocompletion)
    ui.button("Get forecast", on_click=lambda: get_forecast_and_plot())

# Main container that will hold both the graph and weather info
main_container = ui.column().classes("items-center gap-4 w-full")

def get_forecast_and_plot():
    user_input = search_word.value.strip()
    if not user_input:
        ui.notify("Please enter a location", type="warning")
        return

    forecast_data, forecast_status_code = get_weather_forecast(user_input)

    # Clear previous content
    main_container.clear()
    if forecast_status_code != 200:
        if forecast_status_code == 400:
            ui.label(f"Error! Provided location doesn't exist.\nStatus code: {forecast_status_code}")
            return
        ui.label(f"Error! Status code: {forecast_status_code}")
        return

    if not forecast_data:
        ui.label("No forecast data available. Try another location.").style('color: red; font-size: 20px;')
        return

    # Create the plot inside the same column to align it properly
    with main_container:
        with ui.matplotlib(figsize=(9, 4)).figure as fig:
            x = list(forecast_data.keys())
            y = list(forecast_data.values())
            ax = fig.gca()
            ax.plot(x, y, '-')
            ax.set_title(f"Today's temperature for {user_input}")
            ax.set_xlabel("Time")
            ax.set_ylabel("Temperature")

    # Get current weather state
    time_rn, c_temp, c_icon, current_status_code = get_current_state(user_input)
    if current_status_code != 200:
        ui.label(f"Error! Status code: {current_status_code}")
        return

    # Display current weather info centered below the graph
    with main_container:
        ui.label(time_rn)
        ui.markdown(f"### Currently: {c_temp}°C")
        ui.image(c_icon).props("width=50px height=50px")

ui.run()


#if __name__ == "__main__":
    #ui.run()