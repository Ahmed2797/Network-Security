from dataclasses import dataclass,asdict
import pandas as pd

@dataclass
class NetworkSecurity_Features:
    having_ip_address: int
    url_length: int
    shortining_service: int
    having_at_symbol: int
    double_slash_redirecting: int
    prefix_suffix: int
    having_sub_domain: int
    sslfinal_state: int
    domain_registration_length: int
    favicon: int
    port: int
    https_token: int
    request_url: int
    url_of_anchor: int
    links_in_tags: int
    sfh: int
    submitting_to_email: int
    abnormal_url: int
    redirect: int
    on_mouseover: int
    rightclick: int
    popupwindow: int
    iframe: int
    age_of_domain: int
    dnsrecord: int
    web_traffic: int
    page_rank: int
    google_index: int
    links_pointing_to_page: int
    statistical_report: int

    # Convert to dict
    def dict_data(self):
        return asdict(self) 
    # dict-->>--DataFrame
    def dict_data_to_dataframe(self):
        data = pd.DataFrame(self.dict_data())
        return data