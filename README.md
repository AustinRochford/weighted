# weighted ⚖️
Weighted operations for Pandas DataFrames

## Development

### Docker

For easy development and prototyping using [Jupyter notebooks](https://jupyter.org/), a Docker container can be provisioned.  To run a notebook server with access to your development version of `weighted`, run

```bash
> sh ./start_container.sh
```

The notebook server will be available at [http://localhost:8888/tree](http://localhost:8888/tree).  See the beginning of [`start_container.sh`](./start_container.sh) for options that can be passed to the container creation script.

### Testing

`weighted` uses [`hypothesis`](https://hypothesis.readthedocs.io/en/latest/index.html) for generative testing.  To run the tests open a terminal in the Docker container (either through the Jupyter interface or with `docker exec -it weighted bash`) and do

```bash
> cd weighted
> pytest tests/test.py
```
