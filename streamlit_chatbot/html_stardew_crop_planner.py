import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Stardew Valley Crop Planner", layout="wide")
st.title("🌾 Stardew Valley Crop Database Calculator")

# Example crop data (simplified for demo)
crops_data = {
    "Spring": [
        {"Crop": "Parsnip", "Growth Days": 4, "Regrowth": 0},
        {"Crop": "Cauliflower", "Growth Days": 12, "Regrowth": 0},
        {"Crop": "Green Bean", "Growth Days": 10, "Regrowth": 3},
        {"Crop": "Blue Jazz", "Growth Days": 7, "Regrowth": 0},
        {"Crop": "Kale", "Growth Days": 6, "Regrowth": 0}
    ],
    "Summer": [
        {"Crop": "Tomato", "Growth Days": 11, "Regrowth": 4},
        {"Crop": "Blueberry", "Growth Days": 13, "Regrowth": 4},
        {"Crop": "Hot Pepper", "Growth Days": 5, "Regrowth": 3},
        {"Crop": "Summer Spangle", "Growth Days": 8, "Regrowth": 0},
        {"Crop": "Wheat", "Growth Days": 4, "Regrowth": 0}
    ],
    "Fall": [
        {"Crop": "Corn", "Growth Days": 14, "Regrowth": 4},
        {"Crop": "Pumpkin", "Growth Days": 13, "Regrowth": 0},
        {"Crop": "Grape", "Growth Days": 10, "Regrowth": 3},
        {"Crop": "Cranberries", "Growth Days": 7, "Regrowth": 5},
        {"Crop": "Fairy Rose", "Growth Days": 12, "Regrowth": 3}
    ],
    "Winter": []  # No crops grow in winter by default
}

crop_images = {
    "Parsnip": "https://stardewvalleywiki.com/mediawiki/images/d/db/Parsnip.png",
    "Cauliflower": "https://stardewvalleywiki.com/mediawiki/images/a/aa/Cauliflower.png",
    "Green Bean": "https://stardewvalleywiki.com/mediawiki/images/5/5c/Green_Bean.png",
    "Tomato": "https://stardewvalleywiki.com/mediawiki/images/9/9d/Tomato.png",
    "Blueberry": "https://stardewvalleywiki.com/mediawiki/images/9/9e/Blueberry.png",
    "Hot Pepper": "https://stardewvalleywiki.com/mediawiki/images/f/f1/Hot_Pepper.png",
    "Corn": "https://stardewvalleywiki.com/mediawiki/images/f/f8/Corn.png",
    "Pumpkin": "https://stardewvalleywiki.com/mediawiki/images/6/64/Pumpkin.png",
    "Grape": "https://stardewvalleywiki.com/mediawiki/images/c/c2/Grape.png",
    "Blue Jazz": "https://stardewvalleywiki.com/mediawiki/images/2/2f/Blue_Jazz.png",
    "Kale": "https://stardewvalleywiki.com/mediawiki/images/d/d1/Kale.png",
    "Summer Spangle": "https://stardewvalleywiki.com/mediawiki/images/9/9f/Summer_Spangle.png",
    "Wheat": "https://stardewvalleywiki.com/mediawiki/images/e/e2/Wheat.png",
    "Cranberries": "https://stardewvalleywiki.com/mediawiki/images/6/6e/Cranberries.png",
    "Fairy Rose": "https://stardewvalleywiki.com/mediawiki/images/5/5c/Fairy_Rose.png"
}

festival_closures = {
    "Spring": [13, 24],
    "Summer": [11, 28],
    "Fall": [16, 27],
    "Winter": [8, 25],
}

season = st.selectbox("Select Season", ["Spring", "Summer", "Fall", "Winter"])
crop_list = crops_data.get(season, [])
closed_days = festival_closures.get(season, [])

if crop_list:
    crop_names = [crop["Crop"] for crop in crop_list]
    selected_crop = st.selectbox("Filter by Crop (optional)", ["All"] + crop_names)
    day = st.slider("Current Day of the Season", 1, 28, 1)
    show_hidden = st.checkbox("Show hidden crops (not plantable today)", value=False)
    cc_done = st.checkbox("Community Center Complete (Pierre open on Wednesdays)", value=False)

    st.markdown("### Growth Speed Options")
    speed_gro_type = st.radio("Select Fertilizer", ["None", "Speed Gro (+10%)", "Deluxe Speed Gro (+25%)", "Hyper Speed Gro (+33%)"])
    agriculturist = st.checkbox("Agriculturist Profession (+10%)")

    # Determine growth multiplier
    speed_bonus = {
        "None": 0.0,
        "Speed Gro (+10%)": 0.10,
        "Deluxe Speed Gro (+25%)": 0.25,
        "Hyper Speed Gro (+33%)": 0.33,
    }

    bonus = speed_bonus[speed_gro_type]
    if agriculturist:
        bonus += 0.10

    # Helper function for weekday
    def day_to_weekday(day_number):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return weekdays[(day_number - 1) % 7]

    filtered_crops = [crop for crop in crop_list if selected_crop == "All" or crop["Crop"] == selected_crop]

    # Build DataFrame
    table = []
    for crop in filtered_crops:
        name = crop["Crop"]
        base_grow_days = crop["Growth Days"]
        regrowth = crop["Regrowth"]

        effective_grow_days = math.floor(base_grow_days * (1 - bonus))
        effective_grow_days = max(1, effective_grow_days)

        last_day_to_plant = 28 - effective_grow_days
        weekday = day_to_weekday(last_day_to_plant)
        last_day_str = f"{last_day_to_plant} ({weekday})"

        # Add holiday info
        if last_day_to_plant in closed_days:
            last_day_str += "<br>(General store closed)"
            last_day_str = f"<span style='color:lightblue'>{last_day_str}</span>"
        elif weekday == "Wednesday" and not cc_done:
            last_day_str += "<br>(General store closed)"
            last_day_str = f"<span style='color:red'>{last_day_str}</span>"

        good_to_plant = day <= last_day_to_plant
        crop_type = "Regrowing" if regrowth > 0 else "Single Harvest"

        # Calculate harvests from today and harvest days
        harvests_from_today = 0
        harvest_days = []
        harvest_day = day + effective_grow_days

        if regrowth > 0:
            if harvest_day <= 28:
                harvests_from_today += 1
                harvest_days.append(harvest_day)
                next_harvest = harvest_day + regrowth
                while next_harvest <= 28:
                    harvests_from_today += 1
                    harvest_days.append(next_harvest)
                    next_harvest += regrowth
        else:
            while harvest_day <= 28:
                harvests_from_today += 1
                harvest_days.append(harvest_day)
                harvest_day += effective_grow_days

        if good_to_plant or show_hidden:
            img_url = crop_images.get(name, "")
            name_with_img = f"<img src='{img_url}' width='24' style='vertical-align:middle;margin-right:6px;'/> {name}" if img_url else name
            table.append({
                "Crop": name_with_img,
                "Crop Type": crop_type,
                "Days to Grow": effective_grow_days,
                "Last Day to Plant": last_day_str,
                "Good to Plant Today?": "✅" if good_to_plant else "❌",
                "Harvests Remaining (from Today)": harvests_from_today,
                "Harvest Days": ", ".join(map(str, harvest_days))
            })

    df = pd.DataFrame(table)
    st.markdown("""
    <style>
        td {
            white-space: normal !important;
            word-break: break-word !important;
        }
        .dataframe {
            table-layout: fixed;
            width: 100% !important;
        }
        thead th {
            text-align: center !important;
            vertical-align: middle !important;
            word-break: break-word !important;
            white-space: normal !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("No crops grow in Winter by default.")
