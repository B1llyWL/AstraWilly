<script src="https://js.stripe.com/v3/"></script>
<div id = "card-element"></div>
<button id="save-card">{% trans "Save Card" %}</button>

<script>
    const stripe = Stripe('{{ stripe_publishable_key }}');
    const elements = stripe.elements();
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');

    document.getElementById('save-card').addEventListener('click', async() => {
        const { setupIntent, error } = await stripe.confirmCardSetup(
            '{{ client_secret }}',
            { payment_method: {card: cardElement } }
        );
        if (error) {
            console.error(error);
        } else {
            // Карта сохранена, можно обновить UI
            alert('Card saved!');
        }
    });
</script>