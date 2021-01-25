from sec_edgar_downloader import Downloader

# Initialize a downloader instance.
# If no argument is passed to the constructor, the package
# will attempt to locate the user's downloads folder.
dl = Downloader("./13F_filings/Downloads")

dl.get("13F-HR", "0001067983")