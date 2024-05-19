const { Client, Intents } = require('discord.js-selfbot-v13');
const { HttpsProxyAgent } = require('https-proxy-agent');
const chalk = require('chalk');
const fs = require('fs');
const path = require('path');
const config = require('./config.json');

let token;
let mode;
let proxyChoice;
process.argv.forEach(function (val, indx, array) {
    switch (indx) {
        case 2:
            token = val;
        case 3:
            proxyChoice = val;
    }
});

let bot;
if (proxyChoice == 'ON') {
    proxies = (fs.readFileSync(`${path.dirname('.')}../../proxies.txt`, 'utf-8')).split('\r\n');
    let proxy_choice = proxies[Math.floor(Math.random() * proxies.length)].split(':')
    let proxy = proxy_choice.length > 2 ? `http://${proxy_choice[2]}:${proxy_choice[3]}@${proxy_choice[0]}:${proxy_choice[1]}` : `http://${proxy_choice[0]}:${proxy_choice[1]}`
    let agent = new HttpsProxyAgent(proxy)
    bot = new Client({
        intents: [
            Intents.FLAGS.MESSAGE_CONTENT,
            Intents.FLAGS.GUILD_MESSAGES,
            Intents.FLAGS.GUILD_MESSAGE_REACTIONS,
            Intents.FLAGS.DIRECT_MESSAGE_REACTIONS
        ],
        http: { agent: agent }
    });
} else {
    bot = new Client({
        intents: [
            Intents.FLAGS.MESSAGE_CONTENT,
            Intents.FLAGS.GUILD_MESSAGES,
            Intents.FLAGS.GUILD_MESSAGE_REACTIONS,
            Intents.FLAGS.DIRECT_MESSAGE_REACTIONS
        ],
    });
}

bot.on('ready', () => {
    console.log(`  ${chalk.magenta('[+]')}  ${chalk.bold(bot.user.username)} : ${chalk.cyanBright('READY')}`);
})

bot.on('messageCreate', async (msg) => {
    let users = config.users;

    if (!users.length) {
        console.log(`   ${chalk.red('[!]')}  ${chalk.bold('no')} ${chalk.bold.yellow('USER IDS')} ${chalk.bold('specified in config.json.')}`);
        process.exit(2);
    }

    if (users.includes(msg.author.id)) {
        let replied = await msg.fetchReference().catch((err) => { return; });
        let files = [];

        if (msg.attachments) {
            msg.attachments.forEach(attch => {
                files.push(attch.attachment);
            });
        }

        if (replied && files.length) {
            return replied.reply({ content: msg.content ? msg.content : ' ', files: files }).catch((err) => { return; });
        } else if (replied) {
            return replied.reply(msg.content).catch(err => { return; });
        } else if (files.length) {
            return msg.channel.send({ content: msg.content ? msg.content : ' ', files: files }).catch(err => { return; });
        } else {
            return msg.channel.send(msg.content).catch(err => { return; });
        }
    } else return;

});

bot.login(token);