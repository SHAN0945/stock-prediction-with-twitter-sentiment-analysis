export type StockData = {
    name: string;
    symbol: string;
    price: number;
    discriminator_loss: number;
    marketCap: string;
    generator_loss: number;
    test_rmse: number;
    epoch: number;
    pred?: number;
    modelImg?: string;
    predImg?: string;
    lossImg?: string;
    tweets?: string[];
    score: number[];
};

export const stocksData: Record<string, StockData> = {
    msft: {
        name: "Microsoft Corporation",
        symbol: "MSFT",
        price: 384.0,
        discriminator_loss: 1.3713552,
        marketCap: "2.82 trillion",
        generator_loss: 0.6917942,
        test_rmse: 7.6779561276748445,
        epoch: 150,
        pred: 385.64008,
        modelImg: "./public/msft.png",
        predImg: "./public/msft_pred.png",
        lossImg: "./public/lossMsft.png",
        tweets: [
            "Live Sector Flow $spy $aapl $msft $amzn $meta $googl $avgo this are the top flow from spy if you like this post i kindly request to like and subscribe , much love",
            "OpenAI is reportedly developing a new social network similar to X. Consider buying MSFT call options with a 1-2 week expiration. As a major investor in OpenAI, Microsoft's stock could benefit from potential growth and innovation in the social media space. $MSFT",
            "$MSFT favored pullback towards weekly #bluebox area from 3.30.2025 weekend update between 355.33 - 293.08 area, where it should find next support to see at least 3 swing bounce. #Elliottwave #Stocks",
            "TRUMP SAVES APPLE DRIVEN TECH RALLY FROM FAILING, OPPORTUNITIES AHEAD BUT DO NOT BE A HERO - Read more. $AAPL $AMZN $BTCUSD $GOLD $GOOG $GOOGL $META $MSFT $NVDA $OIL $QQQ $SILVER $SPY $TSLA",
            "$GOOGL Daily. More relative weakness from $MAGS ETF names today doesn't inspire much confidence in this low volume bounce yet. Alphabet plus $AMZN $META $MSFT continue to lag market",
        ],
        score: [0.9217, 0.8020, 0.6705, -0.7227, -0.9058],

    },
    aapl: {
        name: "Apple Inc.",
        symbol: "AAPL",
        price: 150.0,
        discriminator_loss: 1.3913552,
        marketCap: "3.28 trillion",
        generator_loss: 0.7017942,
        test_rmse: 6.11477669141758,
        epoch: 500,
        score:[]
    },
};