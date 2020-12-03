import Page from 'material-ui-shell/lib/containers/Page'
import React, {useState} from 'react'
import {Container, Grid, makeStyles} from "@material-ui/core";
import Box from "@material-ui/core/Box";
import TextField from "@material-ui/core/TextField";
import InputAdornment from "@material-ui/core/InputAdornment";
import {SearchRounded} from "@material-ui/icons";
import Button from "@material-ui/core/Button";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import Avatar from "@material-ui/core/Avatar";
import Divider from "@material-ui/core/Divider";
import ListItemText from "@material-ui/core/ListItemText";
import Typography from "@material-ui/core/Typography";
import List from "@material-ui/core/List";

const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: theme.palette.background.dark,
        minHeight: '100%',
        width: '100%',
        paddingBottom: theme.spacing(3),
        paddingTop: theme.spacing(3)
    },
    rootList: {
        width: '100%',
        backgroundColor: theme.palette.background.paper,
    },
    inline: {
        display: 'block',
    },
}));

const SearchText = (callback, deps) => {
    const classes = useStyles();
    const [tweetList, setTweetList] = useState([])
    const [timeStamp, setTimeStamp] = useState('')
    const [searchTextVal, setSearchTextVal] = useState('test')
    const [isFetching, setIsFetching] = useState(false)

    const fetchRequest = () => {
        setIsFetching(true)
        const requestOptions = {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                text: searchTextVal
            })
        };
        console.log(searchTextVal)
        fetch("http://127.0.0.1:5000/searchText", requestOptions)
            .then(res => res.json())
            .then(
                (result) => {
                    setTimeStamp('Time required: ' + result.time_taken + 's')
                    result.data.map((item, idx) => {
                        console.log(item.tweet.text)
                    })
                    setTweetList(result.data)
                    setIsFetching(false)
                }
            )

    };

    return (
        <Page className={classes.root}>

            <Container maxWidth={false}>

                <Grid container>
                    <Box
                        xs={9}
                        sm={9}
                        md={9}
                        lg={9}
                        xl={9}
                        width={.75}
                    >
                        <TextField
                            id="filled-full-width"
                            label="Search Tweet Text Here"
                            style={{margin: 8}}
                            placeholder=""
                            helperText=""
                            fullWidth
                            margin="normal"
                            value={searchTextVal}
                            onChange={e => setSearchTextVal(e.target.value)}
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <SearchRounded/>
                                    </InputAdornment>
                                ),
                            }}
                            variant="filled"
                        />
                    </Box>
                    <Box
                        xs={3}
                        sm={3}
                        md={3}
                        lg={3}
                        xl={3}
                    >
                        <Button variant="contained" color="secondary" style={{margin: 8, marginLeft: 20}}
                                onClick={fetchRequest} disabled={isFetching}>
                            Search
                        </Button>
                    </Box>
                    <Typography>{timeStamp}</Typography>
                    <Box
                        xs={12}
                        sm={12}
                        md={12}
                        lg={12}
                        xl={12}
                        width={1}
                    >
                        <List className={classes.rootList}>
                            {
                                tweetList.map((item, idx) => {
                                    return (
                                        <div id={"list-child-" + idx}>
                                            <ListItem alignItems="flex-start">
                                                <ListItemAvatar>
                                                    <Avatar alt={item.tweet.user_screen_name}
                                                            src="/static/images/avatar/1.jpg"
                                                    />
                                                </ListItemAvatar>
                                                <ListItemText
                                                    primary={(idx+1) + ': ' + item.tweet.user_name}
                                                    secondary={
                                                        <React.Fragment>
                                                            <Typography
                                                                component="span"
                                                                variant="body2"
                                                                className={classes.inline}
                                                                color="textPrimary"
                                                            >
                                                                {item.tweet.text}
                                                            </Typography>
                                                            <Typography>
                                                                {" ~ " + item.tweet.user_screen_name}
                                                            </Typography>
                                                            {item.tweet.entities.hashtags.map((it, idx) => {
                                                                <Typography>#{it}</Typography>
                                                            })}
                                                            <Typography>
                                                                Created at: {item.tweet.created_at.split('+')[0]}
                                                            </Typography>
                                                            <Typography>
                                                                Score: {item.score} Retweets: {item.tweet.retweet_count} Replies: {item.tweet.reply_count}
                                                            </Typography>
                                                        </React.Fragment>
                                                    }
                                                />
                                            </ListItem>
                                            <Divider variant="inset" component="li"/>
                                        </div>)
                                })
                            }
                        </List>
                    </Box>
                </Grid>
            </Container>
        </Page>
    )
}
export default SearchText
