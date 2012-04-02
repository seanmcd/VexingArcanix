<%inherit file="shell.mako" />

<%block name="main_content">
    ${self.confirm_deck()}
</%block>

<%def name="confirm_deck()">
    <p>Here's the data we got from the form: <br>
        <ul id="raw_cards_list">
            % for l in form_data:
            <li>${l}</li>
            % endfor
        </ul>
    </p>
    <hr>
    <p>Here's the deck list we got from that: <br>
        <ul id="parsed_cards_list">
            % for l in parsed_data:
            <li>${l[0]} copies of ${l[1]}</li>
            % endfor
        </ul>

    <h2><a href='/'>Try again.</a></h2>
    <h2><a href='/ask' title="I am not afraid.">Ask me a question, bridgekeeper</a></h2>
</%def>
