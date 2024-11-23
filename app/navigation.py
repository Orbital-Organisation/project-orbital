import streamlit as st


def show_navigation(menu_items):
    """
    Renders a custom navigation sidebar and loads the selected page.

    Args:
        menu_items (dict): A dictionary where keys are menu names and values are tuples (module, title).
                          Example: {"Home": ("pages.page1", "Home Page")}
    """
    st.sidebar.title("Navigation")

    # Display menu items in the sidebar
    selected_page = st.sidebar.radio("Go to", list(menu_items.keys()))

    # Import and execute the main function of the selected page
    page_module, page_title = menu_items[selected_page]
    st.title(page_title)
    
    # Dynamically load the module
    module = __import__(page_module, fromlist=["main"])
    module.main()
