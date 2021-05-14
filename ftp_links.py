#!/usr/bin/env python

# Expects to be run with Python 2.7

import os
import webbrowser
from urllib import quote_plus
from collections import namedtuple

# Assumes there is a folder named brainier-ftp on the Desktop
PDF_ROOT_DIR = '~/Desktop/brainier-ftp'

LINK_URL_TEMPLATE = 'http://foo.bar/pdf/{}'

# tabbed panels - https://codepen.io/markcaron/pen/MvGRYV
# card layout - https://www.w3schools.com/howto/howto_css_cards.asp
HTML_OUTPUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Links</title>
    <style>
        *,
        *:before,
        *:after {
            box-sizing: border-box;
        }
        
        body {
            display: grid;
            place-items: center;
        }
        
        .tabset {
            width: 80em;
        }
        
        .tabset>label {
            position: relative;
            display: inline-block;
            padding: 15px 15px 25px;
            border: 1px solid transparent;
            border-bottom: 0;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            cursor: pointer;
            font-weight: 600;
        }
        
        .tabset>label::after {
            content: "";
            position: absolute;
            left: 15px;
            bottom: 10px;
            width: 22px;
            height: 4px;
            background: #8d8d8d;
        }
        
        .tabset>label:hover,
        .tabset>input:focus+label {
            color: #06c;
        }
        
        .tabset>label:hover::after,
        .tabset>input:focus+label::after,
        .tabset>input:checked+label::after {
            background: #06c;
        }
        
        .tabset>input:checked+label {
            border-color: #ccc;
            border-bottom: 1px solid #fff;
            margin-bottom: -1px;
        }
        
        .tab-panel {
            padding: 30px 1rem;
            border: 1px solid #ccc;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        }
        
        .tab-panel:first-child {
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
            border-bottom-left-radius: 5px;
        }
        
        .tab-panel:not(:first-child) {
            border-radius: 5px;
        }
        
        .tabset>input[type="radio"] {
            position: absolute;
            left: -200vw;
        }
        
        .tabset .tab-panel {
            display: none;
        }
        
        .tabset>input:first-child:checked~.tab-panels>.tab-panel:first-child,
        .tabset>input:nth-child(3):checked~.tab-panels>.tab-panel:nth-child(2),
        .tabset>input:nth-child(5):checked~.tab-panels>.tab-panel:nth-child(3),
        .tabset>input:nth-child(7):checked~.tab-panels>.tab-panel:nth-child(4),
        .tabset>input:nth-child(9):checked~.tab-panels>.tab-panel:nth-child(5),
        .tabset>input:nth-child(11):checked~.tab-panels>.tab-panel:nth-child(6) {
            display: block;
        }
        
        .card {
            /* Add shadows to create the "card" effect */
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            transition: 0.3s;
            border-radius: 5px;
            /* 5px rounded corners */
            padding: 2px 16px;
            margin-top: 1rem;
        }
        /* On mouse-over, add a deeper shadow */
        
        .card:hover {
            box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        }
        
        .card>.channel {
            font-size: 1.5rem;
            font-weight: bold;
            font-style: italic;
        }
        
        .card>.label {
            font-size: 1rem;
            font-weight: bold;
            font-style: italic;
            margin-top: 1rem;
        }
        
        .card>.url {
            margin-top: .5rem;
        }
        
        .card>.link {
            margin-top: 1rem;
        }   
        
        .section-label {
            font-size: 1rem;
            font-weight: bold;
            text-decoration: underline;
        }
    </style>
</head>
<body>
<div class="tabset">
    %(tabset)s
    <div class="tab-panels">
        %(panels)s
    </div>
</div>
</body>
</html>
"""

TAB_TEMPLATE = """
<input type="radio" name="tabset" id="{channel}" aria-controls="{channel}" {checked}>
<label for="{channel}">{channel}</label>
"""

TAB_PANEL_TEMPLATE = """
<section class="tab-panel">
    <div class="section-label">{channel}</div>
    {link_cards}
</section>
"""

LINK_OUTPUT_TEMPLATE = """
<div class="card">
    <div class="label">{label}</div>
    <div class="url">{url}</div>
    <div class="link">Test the link: <a href="{url}">{label}</a></div>
</div>
"""

Link = namedtuple('Link', ['channel', 'label', 'url'])


def create_link(sub_dir, pdf):
    """
    Creates the channel based on the sub_dir name
    Creates the label based on the pdf name
    Urlencodes the sub_dir and pdf names if necessary

    Example
    >>> create_link('speciality stuff', 'oNe fine summer Day.pdf')
    Link(channel='speciality stuff', label='one fine summer day', url='http://foo.bar/pdf/speciality+stuff/one+fine+summer+day.pdf')
    """
    # the category is the sub_dir name
    channel = sub_dir.lower()

    # fix the filename, lowercase and replace spaces with underscores
    # pdf = pdf.replace(' ', '_').lower()

    # create the label based on the pdf name
    label = pdf.replace('.pdf', '').replace('_', ' ').lower()

    # construct the url
    urlencoded_pdf_path = '{}/{}'.format(quote_plus(sub_dir), quote_plus(pdf))
    url = LINK_URL_TEMPLATE.format(urlencoded_pdf_path).lower()

    return Link(channel, label, url)


def create_card(link):
    return LINK_OUTPUT_TEMPLATE.format(**link._asdict())


def create_html(links, output_file):
    tabset = []
    panels = []
    data = {}
    for link in links:
        channel = data.get(link.channel, [])
        channel.append(create_card(link))
        data[link.channel] = channel

    checked = 'checked'
    for channel, panel in data.items():
        tabset.append(TAB_TEMPLATE.format(channel=channel, checked=checked))
        panels.append(TAB_PANEL_TEMPLATE.format(channel=channel, link_cards=''.join(panel)))
        if checked:
            checked = ''

    html = HTML_OUTPUT_TEMPLATE % {'tabset': ''.join(tabset), 'panels': ''.join(panels)}
    with open(output_file, 'w') as f:
        f.write(html)


def main():
    pdf_root = os.path.expanduser(PDF_ROOT_DIR)

    # create links for each of the pdfs in each sub-directory
    # assumes all pdfs are in exactly 1 level of sub-directories
    links = [
        create_link(sub_dir, f)
        for sub_dir in os.listdir(pdf_root) if os.path.isdir(os.path.join(pdf_root, sub_dir))
        for f in os.listdir(os.path.join(pdf_root, sub_dir)) if f.endswith('.pdf')
    ]

    # save the output to an html file for viewing
    html_file = os.path.join(pdf_root, 'links.html')
    create_html(links, html_file)

    # open the links.html file in the browser window
    webbrowser.open_new_tab(html_file)


if __name__ == '__main__':
    main()
