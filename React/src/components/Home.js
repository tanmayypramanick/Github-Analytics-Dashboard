// Import required libraries
import * as React from "react";
import { useState } from "react";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import AppBar from "@mui/material/AppBar";
import CssBaseline from "@mui/material/CssBaseline";
import Toolbar from "@mui/material/Toolbar";
import BarCharts from "./BarCharts";
import StarBarCharts from "./StarBarCharts";
import ForkBarCharts from "./ForkBarCharts";
import List from "@mui/material/List";
import LineCharts from "./LineCharts";
import StackBar from "./StackBar";
import Loader from "./Loader";
import { ListItemButton } from "@mui/material";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";

const drawerWidth = 240;
const repositories = [
  {
    key: "langchain-ai/langchain",
    value: "LangChain",
  },
  {
    key: "langchain-ai/langgraph",
    value: "LangGraph",
  },
  {
    key: "microsoft/autogen",
    value: "AutoGen",
  },
  {
    key: "openai/openai-cookbook",
    value: "Openai-Cookbook",
  },
  {
    key: "elastic/elasticsearch",
    value: "Elasticsearch",
  },
  {
    key: "milvus-io/pymilvus",
    value: "Pymilvus",
  },
  {
    key: "X langchain-ai/langchain langchain-ai/langgraph microsoft/autogen openai/openai-cookbook elastic/elasticsearch milvus-io/pymilvus",
    value: "Number of stars",
  },
  {
    key: "Y langchain-ai/langchain langchain-ai/langgraph microsoft/autogen openai/openai-cookbook elastic/elasticsearch milvus-io/pymilvus",
    value: "Number of forks",
  },
];

export default function Home() {
  const [loading, setLoading] = useState(true);

  const [repository, setRepository] = useState({
    key: "langchain-ai/langchain",
    value: "LangChain",
  });

  //setting conditions for stars and forks as false by default,
  const [isStars, setIsStars] = useState("false");
  const [isForks, setIsForks] = useState("false");
  const [flag, setFlag] = useState("true");

  const [githubRepoData, setGithubData] = useState([]);
  // Updates the repository to newly selected repository
  const eventHandler = (repo) => {
    setRepository(repo);
  };

  React.useEffect(() => {
    // set loading to true to display loader
    setLoading(true);
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // Append the repository key to request body
      body: JSON.stringify({ repository: repository.key }),
    };
    //fetch("")
    //setIsStar(true)

    fetch("/api/github", requestOptions)
      .then((res) => res.json())
      .then(
        // On successful response from flask microservice
        (result) => {
          // On success set loading to false to display the contents of the resonse
          setLoading(false);

          if (result.stars !== undefined && result.forks == undefined) {
            setIsStars(true);
            setIsForks(false);
            setFlag(false);
            setGithubData(result);
            console.log("Instars-stars: ", isStars);
            console.log("Instars-forks: ", isForks);
          } else if (result.forks !== undefined && result.stars == undefined) {
            setIsForks(true);
            setIsStars(false);
            setFlag(false);
            setGithubData(result);
            console.log("Infork-stars: ", isStars);
            console.log("Infork-forks: ", isForks);
          } else {
            setFlag(true);
            setIsStars(false);
            setIsForks(false);
            console.log("chek");
            // Set state on successfull response from the API
            setGithubData(result);
          }
        },
        // On failure from flask microservice
        (error) => {
          // Set state on failure response from the API
          console.log(error);
          // On failure set loading to false to display the error message
          setLoading(false);
          setGithubData([]);
        }
      );
  }, [repository]);

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      {/* Application Header */}
      <AppBar
        position='fixed'
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant='h6' noWrap component='div'>
            Timeseries Forecasting
          </Typography>
        </Toolbar>
      </AppBar>
      {/* Left drawer of the application */}
      <Drawer
        variant='permanent'
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: "auto" }}>
          <List>
            {/* Iterate through the repositories list */}
            {repositories.map((repo) => (
              <ListItem
                button
                key={repo.key}
                onClick={() => eventHandler(repo)}
                disabled={loading && repo.value !== repository.value}
              >
                <ListItemButton selected={repo.value === repository.value}>
                  <ListItemText primary={repo.value} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
      <Box component='main' sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {/* Render loader component if loading is true else render charts and images */}
        {loading ? (
          <Loader />
        ) : (
          <div>
            {/* Render linechart component for weekly created issues for a selected repositories*/}
            {flag && (
              <LineCharts
                title={`Issues of ${repository.value} in last 2 years`}
                data={githubRepoData?.created_weekly}
              />
            )}

            {/* Render barchart component for monthly created issues for a selected repositories*/}
            {flag && (
              <BarCharts
                title={`Monthly Created Issues of ${repository.value} in last 2 years`}
                data={githubRepoData?.created}
              />
            )}

            {/* Render barchart component for weekly closed issues for a selected repositories*/}
            {flag && (
              <BarCharts
                title={`Weekly Closed Issues of ${repository.value} in last 2 years`}
                data={githubRepoData?.closed_weekly}
              />
            )}

            {/* Render stackbar component for created and closed issues*/}
            {flag && (
              <StackBar
                title={`Created and Closed Issues of ${repository.value} in last 2 years`}
                data={githubRepoData?.created}
                data2={githubRepoData?.closed}
              />
            )}

            {isStars && (
              <StarBarCharts
                title={`Number of stars for each repository`}
                data={githubRepoData?.stars}
              />
            )}
            {isForks && (
              <ForkBarCharts
                title={`Number of forks for each repository`}
                data={githubRepoData?.forks}
              />
            )}
            {flag && (
              <div>
                <Divider
                  sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
                />
                <div>
                  <Typography variant='h5' component='div' gutterBottom>
                    The day of the week maximum number of issues created
                  </Typography>
                  <div>
                    <img
                      src={
                        githubRepoData?.createdAtImageUrls
                          ?.day_max_issue_created
                      }
                      alt={
                        "The day of the week maximum number of issues created"
                      }
                      loading={"lazy"}
                    />
                  </div>
                </div>
                <div>
                  <Typography variant='h5' component='div' gutterBottom>
                    The day of the week maximum number of issues Closed
                  </Typography>
                  <div>
                    <img
                      src={
                        githubRepoData?.createdAtImageUrls?.day_max_issue_closed
                      }
                      alt={
                        "The day of the week maximum number of issues Closed"
                      }
                      loading={"lazy"}
                    />
                  </div>
                </div>

                <div>
                  <Typography variant='h5' component='div' gutterBottom>
                    The month of the year that has maximum number of issues
                    closed
                  </Typography>
                  <div>
                    <img
                      src={
                        githubRepoData?.createdAtImageUrls
                          ?.month_max_issues_closed
                      }
                      alt={
                        "The month of the year that has maximum number of issues closed"
                      }
                      loading={"lazy"}
                    />
                  </div>
                </div>
              </div>
            )}

            <Divider
              sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
            />
            {/* Rendering Timeseries Forecasting of Created Issues using Tensorflow and
                Keras LSTM */}

            {/* Rendering Timeseries Forecasting of Closed Issues using Tensorflow and
                Keras LSTM  */}
            {flag && (
              <div>
                <Divider
                  sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
                />
                <Typography variant='h5' component='div' gutterBottom>
                  Timeseries Forecasting of Closed Issues using Tensorflow and
                  Keras LSTM based on past month
                </Typography>

                <div>
                  <Typography component='h4'>
                    Model Loss for Closed Issues
                  </Typography>
                  {/* Render the model loss image for closed issues  */}
                  {
                    <img
                      src={
                        githubRepoData?.closedAtImageUrls?.model_loss_image_url
                      }
                      alt={"Model Loss for Closed Issues"}
                      loading={"lazy"}
                    />
                  }
                </div>
                <div>
                  <Typography component='h4'>
                    LSTM Generated Data for Closed Issues
                  </Typography>
                  {/* Render the LSTM generated image for closed issues */}
                  {
                    <img
                      src={
                        githubRepoData?.closedAtImageUrls
                          ?.lstm_generated_image_url
                      }
                      alt={"LSTM Generated Data for Closed Issues"}
                      loading={"lazy"}
                    />
                  }
                </div>
                <div>
                  <Typography component='h4'>
                    All Issues Data for Closed Issues
                  </Typography>
                  {/* Render the all issues data image for closed issues*/}
                  <img
                    src={
                      githubRepoData?.closedAtImageUrls?.all_issues_data_image
                    }
                    alt={"All Issues Data for Closed Issues"}
                    loading={"lazy"}
                  />
                </div>
              </div>
            )}

            {flag && (
              <div>
                <Divider
                  sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
                />
                <Typography variant='h5' component='div' gutterBottom>
                  Timeseries Forecasting of Pull Requests using Tensorflow and
                  Keras LSTM based on past month
                </Typography>

                <div>
                  <Typography component='h4'>
                    Model Loss for Pull Requests
                  </Typography>
                  {/* Render the model loss image Pull Requests  */}
                  <img
                    src={githubRepoData?.pullReqImageUrls?.model_loss_image_url}
                    alt={"Model Loss for Pull Requests"}
                    loading={"lazy"}
                  />
                </div>
                <div>
                  <Typography component='h4'>
                    LSTM Generated Data for Pull Requests
                  </Typography>
                  {/* Render the LSTM generated image Pull Requests */}
                  <img
                    src={
                      githubRepoData?.pullReqImageUrls?.lstm_generated_image_url
                    }
                    alt={"LSTM Generated Data for Pull Requests"}
                    loading={"lazy"}
                  />
                </div>
              </div>
            )}
            {/* Rendering Timeseries Forecasting of Commits using Tensorflow and
                Keras LSTM  */}
            {flag && (
              <div>
                <Divider
                  sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
                />
                <Typography variant='h5' component='div' gutterBottom>
                  Timeseries Forecasting of Commits using Tensorflow and Keras
                  LSTM based on past month
                </Typography>

                <div>
                  <Typography component='h4'>Model Loss for Commits</Typography>
                  {/* Render the model loss image Commits  */}
                  <img
                    src={githubRepoData?.commitsImageUrls?.model_loss_image_url}
                    alt={"Model Loss for Commits"}
                    loading={"lazy"}
                  />
                </div>
                <div>
                  <Typography component='h4'>
                    LSTM Generated Data for Commits
                  </Typography>
                  {/* Render the LSTM generated image Commits */}
                  <img
                    src={
                      githubRepoData?.commitsImageUrls?.lstm_generated_image_url
                    }
                    alt={"LSTM Generated Data for Commits"}
                    loading={"lazy"}
                  />
                </div>
                <div>
                  <Typography component='h4'>
                    All Issues Data for Commits
                  </Typography>
                  {/* Render the all issues data image for Commits*/}
                  <img
                    src={
                      githubRepoData?.commitsImageUrls?.all_issues_data_image
                    }
                    alt={"All Issues Data for Commits"}
                    loading={"lazy"}
                  />
                </div>
              </div>
            )}

            {flag && (
              <div>
                <Divider
                  sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
                />
                <Typography variant='h5' component='div' gutterBottom>
                  Timeseries Forecasting of Created Issues using
                  Facebook/Prophet based on past months
                </Typography>

                <div>
                  <Typography component='h4'>
                    Forecast of Created Issues
                  </Typography>
                  {/* Render the model loss image Created AT  */}
                  <img
                    src={
                      githubRepoData?.fb_createdAtImageUrls
                        ?.fbprophet_forecast_url
                    }
                    alt={"Forecast of Created Issues"}
                    loading={"lazy"}
                  />
                </div>
              </div>
            )}

            {flag && (
              <div>
                <Divider
                  sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
                />
                <Typography variant='h5' component='div' gutterBottom>
                  Timeseries Forecasting of Pull Request using Facebook/Prophet
                  based on past months
                </Typography>

                <div>
                  <Typography component='h4'>
                    Forecast of Pull Request
                  </Typography>
                  {/* Render the model loss image Closed AT  */}
                  <img
                    src={
                      githubRepoData?.fb_pullReqImageUrls
                        ?.fbprophet_forecast_url
                    }
                    alt={"Forecast of Pull Request"}
                    loading={"lazy"}
                  />
                </div>
                <div>
                  <Typography component='h4'>
                    Forecast Components of Pull Request
                  </Typography>
                  {/* Render the LSTM generated image Closed At */}
                  <img
                    src={
                      githubRepoData?.fb_pullReqImageUrls
                        ?.fbprophet_forecast_components_url
                    }
                    alt={"Forecast Components of Pull Request"}
                    loading={"lazy"}
                  />
                </div>
              </div>
            )}

            {flag && (
              <div>
                <Divider
                  sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
                />
                <Typography variant='h5' component='div' gutterBottom>
                  Timeseries Forecasting of Created Issues using StatsModel
                  based on past months
                </Typography>

                <div>
                  <Typography component='h4'>
                    Observation Graph of Created Issues
                  </Typography>
                  {/* Render the model loss image Created AT  */}
                  <img
                    src={
                      githubRepoData?.stat_createdAtImageUrls
                        ?.stats_observation_url
                    }
                    alt={"Observation Graph of Created Issues"}
                    loading={"lazy"}
                  />
                </div>
                <div>
                  <Typography component='h4'>
                    Time Series Forecasting of Created Issues
                  </Typography>
                  {/* Render the LSTM generated image Created At */}
                  <img
                    src={
                      githubRepoData?.stat_createdAtImageUrls
                        ?.stats_forecast_url
                    }
                    alt={"Time Series Forecasting of Created Issues"}
                    loading={"lazy"}
                  />
                </div>
              </div>
            )}

            {flag && (
              <div>
                <Divider
                  sx={{ borderBlockWidth: "3px", borderBlockColor: "#FFA500" }}
                />
                <Typography variant='h5' component='div' gutterBottom>
                  Timeseries Forecasting of Commits Issues using StatsModel
                  based on past months
                </Typography>

                <div>
                  <Typography component='h4'>
                    Observation Graph of Commits Issues
                  </Typography>
                  {/* Render the model loss image Commits  */}
                  <img
                    src={
                      githubRepoData?.stat_commitsImageUrls
                        ?.stats_observation_url
                    }
                    alt={"Observation Graph of Commits Issues"}
                    loading={"lazy"}
                  />
                </div>
                <div>
                  <Typography component='h4'>
                    Time Series Forecasting of Commits Issues
                  </Typography>
                  {/* Render the LSTM generated image Closed At */}
                  <img
                    src={
                      githubRepoData?.stat_commitsImageUrls?.stats_forecast_url
                    }
                    alt={"Forecast Components of Commits"}
                    loading={"lazy"}
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </Box>
    </Box>
  );
}
