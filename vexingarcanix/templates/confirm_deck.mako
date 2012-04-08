<%inherit file="shell.mako" />

<%block name="main_content">
    ${self.confirm_deck()}
</%block>

<%def name="confirm_deck()">
    <p>We think that this is a ${game_guess} deck with the following cards: <br>
        <ul id="parsed_cards_list">
            % for card in deck.decklist:
            <li>${card.count} copies of ${card.name}</li>
            % endfor
        </ul>
    % if unknown_cards:
    <p class="unknown_cards">But we couldn't identify the following:
        <ul id="unknown_cards_list">
            % for card in unknown_cards:
            <li>${card}</li>
            % endfor
        </ul>
    </p>
    % endif

    <hr>

    <h2><a href='/'>Try again.</a></h2>
    <h2><a href='/ask' title="I am not afraid.">Ask me a question, bridgekeeper</a></h2>
</%def>
