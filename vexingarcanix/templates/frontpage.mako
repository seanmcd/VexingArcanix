<%inherit file="shell.mako" />

<%block name="main_content">
    ${self.deck_upload()}
</%block>

<%def name="deck_upload()">
    <div id="deck_form" style="margin: auto; text-align: center;">
        <h2>Please enter a deck</h2>
        <hr>
        <form action="/check" method="post">
            <textarea rows="25" cols="40" name="deck_list_area" id="deck_list">
15 Lightning Bolt
15 Grizzly Bears
5 Fireball
5x Gruul Signet'
5 Mountains
5xForest
5   Fire-Lit Thicket
5 "Rootbound Crag"</textarea>
            <br>
            <input type="submit" value="Upload this decklist">
        </form>
    </div>
</%def>
