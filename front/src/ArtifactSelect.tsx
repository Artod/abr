import { gql, useQuery, useLazyQuery } from '@apollo/client';
import {
  Button,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent
} from '@mui/material';

import { useParams } from 'react-router-dom';

const FormattedMessage = (props) => {
  return <span>{props.id}</span>
}

type DeployParams = {
  runId: string;
};
type RunData = any;
type DownloadData = any;

const GET_RUN_ARTIFACTS = gql`
  query GetRunArtifacts($runId: String!) {
    run(_id: $runId) {
      _id
      artifacts {
        _id
        name
      }
    } 
  } 
`;

const DOWNLOAD_ARTIFACT = gql`
  query DownloadArtifact($id: String!) {
    downloadArtifact(_id: $id)
  }
`;

interface ArtifactProps {
  selectedArtifact: string;
  onChange?: (e: SelectChangeEvent<string>) => void;
}

function saveFile(data) {
  const download = document.createElement("a");
  download.href = "data:text/plain;base64," + data.downloadArtifact;
  download.download = "artifact.zip";
  download.click();
}

const ArtifactSelect = (props: ArtifactProps): JSX.Element => {
  const { selectedArtifact, onChange } = props;
  const { runId } = useParams<keyof DeployParams>();

  const { loading: runLoading, data: runData } = useQuery<RunData>(
    GET_RUN_ARTIFACTS,
    {
      variables: { runId },
    }
  );
  const [downloadArtifact, { loading: downloadLoading }] =
    useLazyQuery<DownloadData>(DOWNLOAD_ARTIFACT, {
      onCompleted: (data) => {
        saveFile(data);
      }
    });

  if (runLoading) {
    return <CircularProgress />;
  }

  return (
    <>
      <FormControl className="form-control large-input">
        <InputLabel id="artifact-select-label">
          <FormattedMessage id="deploy.download.format" />
        </InputLabel>
        <Select
          onChange={onChange}
          labelId="artifact-select-label"
          value={selectedArtifact}
        >
          {runData?.run.artifacts.map((artifact) => (
            <MenuItem key={artifact._id} value={artifact._id}>
              <FormattedMessage
                id={"deploy.download.format." + artifact.name.toLowerCase()}
              />
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {!downloadLoading && (
        <FormControl className="form-control large-input button-container">
          <Button
            variant="contained"
            className="button primary"
            color="primary"
            onClick={() => {
              downloadArtifact({
                variables: { id: selectedArtifact },
              });
            }}
          >
            <FormattedMessage id="deploy.button.download" />
          </Button>
        </FormControl>
      )}
      
      {downloadLoading && <CircularProgress />}
    </>
  );
};

export default ArtifactSelect;
